import json, pathlib, urllib.request, os, re

# Paths
BASE_DIR = pathlib.Path(__file__).parent
RAW_DIR = BASE_DIR / 'raw'
MANIFEST_PATH = BASE_DIR / 'manifest.json'
CANDIDATES_PATH = BASE_DIR / 'candidates.json'

# Helper to infer journal from DOI
def infer_journal(doi: str) -> str:
    if '10.1371' in doi:
        return 'PLOS ONE'
    if '10.3389' in doi:
        return 'Frontiers in Psychology'
    return ''

def load_candidates():
    with open(CANDIDATES_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def ensure_journal_fields(candidates):
    for cand in candidates:
        if not cand.get('journal'):
            cand['journal'] = infer_journal(cand.get('doi', ''))
    return candidates

def download_pdfs(candidates):
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    for cand in candidates:
        url = cand.get('pdf_url') or cand.get('oa_url')
        if not url:
            continue
        fname = pathlib.Path(url).name
        if not fname.lower().endswith('.pdf'):
            fname = fname + '.pdf'
        out_path = RAW_DIR / fname
        # skip if already downloaded
        if out_path.is_file():
            status = 'already_exists'
        else:
            try:
                urllib.request.urlretrieve(url, out_path)
                status = 'success'
            except Exception as e:
                status = f'failed ({e})'
        manifest.append({
            'filename': fname,
            'title': cand.get('title',''),
            'doi': cand.get('doi',''),
            'journal': cand.get('journal',''),
            'year': cand.get('year'),
            'source_url': url,
            'download_status': status
        })
    return manifest

def main():
    candidates = load_candidates()
    candidates = ensure_journal_fields(candidates)
    # sort by keyword_score desc then year desc
    candidates.sort(key=lambda x: (-x.get('keyword_score', 0), -(x.get('year') or 0)))
    manifest = download_pdfs(candidates[:40])
    # write back enriched candidates (optional)
    with open(CANDIDATES_PATH, 'w', encoding='utf-8') as f:
        json.dump(candidates, f, indent=2)
    with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    print('Fetch complete. Manifest written to', MANIFEST_PATH)

if __name__ == '__main__':
    main()

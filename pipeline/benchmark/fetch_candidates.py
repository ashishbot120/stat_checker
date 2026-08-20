import json, urllib.request, os, re

KEYWORDS = [
    "study", "experiment", "effect", "association", "intervention",
    "participants", "emotion", "memory", "attention", "behavior",
    "anxiety", "depression"
]
EXCLUDE = ["review", "meta-analysis", "meta analysis", "protocol", "commentary", "qualitative"]

def score_title(title):
    t = title.lower()
    return sum(kw in t for kw in KEYWORDS)

def fetch(source_id):
    base = f"https://api.openalex.org/works?filter=primary_location.source.id:{source_id},open_access.is_oa:true,type:article&per-page=200"
    results = []
    url = base
    while url:
        with urllib.request.urlopen(url) as resp:
            data = json.load(resp)
        results.extend(data.get('results', []))
        # OpenAlex provides a next cursor via meta.next_cursor
        meta = data.get('meta', {})
        cursor = meta.get('next_cursor')
        if cursor:
            url = f"https://api.openalex.org/works?filter=primary_location.source.id:{source_id},open_access.is_oa:true,type:article&per-page=200&cursor={urllib.parse.quote(cursor)}"
        else:
            url = None
    return results

def main():
    candidates = {}
    for sid in ["S202381698", "S9692511"]:
        for work in fetch(sid):
            title = work.get('title', '')
            if any(exc in title.lower() for exc in EXCLUDE):
                continue
            score = score_title(title)
            if score == 0:
                continue
            doi = work.get('doi')
            if not doi:
                continue
            # Deduplicate by DOI, keep highest score
            if doi in candidates and candidates[doi]['keyword_score'] >= score:
                continue
            pdf_url = work.get('open_access', {}).get('pdf_url')
            oa_url = work.get('primary_location', {}).get('source', {}).get('url')
            candidates[doi] = {
                "title": title,
                "doi": doi,
                "journal": work.get('host_venue', {}).get('display_name', ''),
                "year": work.get('publication_year'),
                "pdf_url": pdf_url,
                "oa_url": oa_url,
                "keyword_score": score
            }
    sorted_candidates = sorted(candidates.values(), key=lambda x: -x['keyword_score'])
    out_path = os.path.join(os.path.dirname(__file__), "candidates.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(sorted_candidates, f, indent=2)

if __name__ == "__main__":
    main()

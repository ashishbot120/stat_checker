import json, pathlib, os

# Paths
cand_path = pathlib.Path('pipeline/benchmark/candidates.json')
manifest_path = pathlib.Path('pipeline/benchmark/manifest.json')

# Load candidates
candidates = json.load(open(cand_path))
# Update journal based on DOI prefix
for c in candidates:
    doi = c.get('doi','')
    if '10.1371' in doi:
        c['journal'] = 'PLOS ONE'
    elif '10.3389' in doi:
        c['journal'] = 'Frontiers in Psychology'
    else:
        c['journal'] = ''
# Save updated candidates
with open(cand_path, 'w', encoding='utf-8') as f:
    json.dump(candidates, f, indent=2)

# Load manifest
if manifest_path.exists():
    manifest = json.load(open(manifest_path))
    # Build DOI->journal map
    doi2journal = {c['doi']: c['journal'] for c in candidates}
    for entry in manifest:
        entry['journal'] = doi2journal.get(entry.get('doi',''), '')
    # Save updated manifest
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    # Count per journal among downloaded entries
    counts = {'PLOS ONE':0, 'Frontiers in Psychology':0}
    for e in manifest:
        if e.get('download_status')=='success':
            j = e.get('journal','')
            if j in counts:
                counts[j] += 1
    print('Journal counts among downloaded PDFs:', counts)
else:
    print('manifest.json not found')

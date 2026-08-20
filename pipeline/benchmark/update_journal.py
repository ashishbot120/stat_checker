import json, pathlib, urllib.request, os, sys

# Load candidates
cand_path = pathlib.Path('pipeline/benchmark/candidates.json')
candidates = json.load(open(cand_path))

# Update journal field based on source ID (we stored source ID in a new field earlier)
# Since original data didn't store source ID, we infer from DOI prefix mapping (PLOS ONE DOIs start with 10.1371)
for c in candidates:
    doi = c.get('doi','')
    if doi.startswith('https://doi.org/10.1371'):
        c['journal'] = 'PLOS ONE'
    else:
        c['journal'] = 'Frontiers in Psychology'

# Overwrite candidates.json with updated journal info
with open(cand_path, 'w', encoding='utf-8') as f:
    json.dump(candidates, f, indent=2)

print('Journal fields updated')

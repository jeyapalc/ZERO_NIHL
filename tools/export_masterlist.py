"""Export one cited masterlist per project without manufacturing translations."""
import csv
import io
import json


def export_masterlist(root):
    is_naz = (root / 'data/entries.json').exists()
    filename = 'entries.json' if is_naz else 'terms.json'
    records = {r['id']: r for r in json.loads((root / 'data' / filename).read_text(encoding='utf-8'))}
    sources = {s['id']: s for s in json.loads((root / 'data/sources.json').read_text(encoding='utf-8'))}
    with (root / 'lists/terms_excel.tsv').open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream, delimiter='\t'))
    for row in rows:
        record = records[row['entry_id']]
        refs = [sources[sid] for sid in record['source_ids']]
        row['evidence_basis'] = record.get('evidence_basis', 'documented_association; see sources and context')
        if not is_naz and row['language'] == 'de' and record.get('german_basis', '').startswith('project_translation'):
            row['evidence_basis'] = 'project_translation; not evidence of Canadian usage'
        row['reviewed_at'] = record['reviewed_at']
        row['source_ids'] = ','.join(record['source_ids'])
        # Keep the complete source records in data/sources.json, not each spreadsheet row.
    fields = ['term','enabled','context_note','source_urls','entry_id','language','tier','category','evidence_basis','reviewed_at','source_ids']
    buffer = io.StringIO(newline='')
    writer = csv.DictWriter(buffer, fieldnames=fields, delimiter='\t', lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    (root / 'lists/masterlist.tsv').write_text(buffer.getvalue(), encoding='utf-8-sig', newline='\n')
    terms = sorted({r['term'] for r in rows}, key=lambda value: (value.casefold(), value))
    (root / 'lists/masterlist.txt').write_text('\n'.join(terms)+'\n', encoding='utf-8', newline='\n')
    print(f'Masterlist: {len(rows)} cited rows / {len(terms)} distinct spellings')

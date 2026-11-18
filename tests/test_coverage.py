"""Independently reconcile every literal term and its citations."""
from collections import Counter
import csv
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def read_json(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))

def read_tsv(path):
    with (ROOT / path).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream, delimiter='\t'))

class CoverageTests(unittest.TestCase):
    def test_all_literal_terms_and_sources(self):
        sources = {s['id']: s for s in read_json('data/sources.json')}
        expected = []
        if (ROOT / 'data/entries.json').exists():
            records = read_json('data/entries.json')
            for r in records:
                if r['modality'] == 'visual_only' or r['category'] == 'typographic_pattern':
                    continue
                expected.extend((t, r['id'], ','.join(r['languages'])) for t in [r['term'], *r['aliases']])
        else:
            records = read_json('data/terms.json')
            for r in records:
                expected.extend((t, r['id'], language) for language, terms in r['terms'].items() for t in terms)
        by_id = {r['id']: r for r in records}
        for filename in ('lists/terms_excel.tsv', 'lists/masterlist.tsv'):
            rows = read_tsv(filename)
            self.assertEqual(Counter((r['term'],r['entry_id'],r['language']) for r in rows), Counter(set(expected)))
            for row in rows:
                record = by_id[row['entry_id']]
                self.assertEqual(row['source_urls'].split(), [sources[s]['url'] for s in record['source_ids']])
                self.assertTrue(row['source_urls'])
                if filename.endswith('masterlist.tsv'):
                    self.assertEqual(row['source_ids'].split(','), record['source_ids'])
        lines = (ROOT / 'lists/masterlist.txt').read_text(encoding='utf-8').splitlines()
        self.assertEqual(set(lines), {term for term, _, _ in expected})
        self.assertEqual(len(lines), len(set(lines)))

    def test_registry_names_and_citations(self):
        expected = {(r['id'],r['name'],r['language'],r['source_url']) for r in read_json('data/canada/lte_entities.json')}
        actual = [(r['entry_id'],r['term'],r['language'],r['source_url']) for r in read_tsv('lists/canada_lte_excel.tsv')]
        self.assertEqual(set(actual), expected)
        self.assertEqual(len(actual), len(expected))

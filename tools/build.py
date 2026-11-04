"""Validate records and generate review vocabulary, CSV and catalog."""
import csv
import io
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from zero_nihl import normalize

def build():
    data={name:json.loads((ROOT/'data'/f'{name}.json').read_text()) for name in ['sources','terms','indicators']}
    sources={s['id']:s for s in data['sources']}
    assert len(sources)==len(data['sources'])
    for source in sources.values():
        assert source['url'].startswith('https://') and source['evidence_access']
    for kind in ['terms','indicators']:
        records=data[kind]
        assert len({r['id'] for r in records})==len(records)
        for r in records:
            assert r['source_ids'] and set(r['source_ids'])<=sources.keys(),r['id']
            assert r['action']=='human_review'
            assert r['scope'] in {'nve_related','general_targeted_violence','framework_only'}
            assert r['status']=='initial_research'
            assert r['evidence_basis']
            if kind=='terms':
                assert set(r['terms'])=={'en','de'}
                assert any(r['terms'].values())
                assert all(isinstance(t,str) and t.strip() for v in r['terms'].values() for t in v)
            else:
                assert r['automated_inference'] is False
                assert r['evidence_needed']
        buf=io.StringIO(newline='')
        fields=list(records[0])
        w=csv.DictWriter(buf,fieldnames=fields)
        w.writeheader()
        for r in records:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()})
        (ROOT/'data'/f'{kind}.csv').write_text(buf.getvalue())
    out=ROOT/'lists'
    out.mkdir(exist_ok=True)
    for language in ['en','de']:
        values={normalize(t) for r in data['terms'] for t in r['terms'][language]}
        (out/f'{language}_contextual.txt').write_text('\n'.join(sorted(values))+'\n')
    lines=['# ZERO_NIHL catalog','','All terms are context-dependent retrieval vocabulary. Observation prompts require direct evidence and qualified human assessment. No risk scores or framework item coding.','','## Terms','','| ID | English | German (project translations) | Scope | Evidence | Sources |','| --- | --- | --- | --- | --- | --- |']
    def refs(record):return ', '.join(f"[{id}]({sources[id]['url']})" for id in record['source_ids'])
    for r in data['terms']:
        lines.append('| '+' | '.join([r['id'],', '.join(r['terms']['en']),', '.join(r['terms']['de']),r['scope'],r['evidence_basis'],refs(r)])+' |')
    lines+=['','## Observation prompts','','| ID | Label | Observation | Sources |','| --- | --- | --- | --- |']
    for r in data['indicators']:lines.append('| '+' | '.join([r['id'],r['label'],r['summary'],refs(r)])+' |')
    (ROOT/'CATALOG.md').write_text('\n'.join(lines)+'\n')
    print(f"Validated {len(data['terms'])} term records, {len(data['indicators'])} prompts, {len(sources)} sources")

if __name__=='__main__':
    build()
    from export_review import export
    export(ROOT)

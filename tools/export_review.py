"""Generate readable and Excel-friendly review references."""
import csv,io,json

def export(root):
    sources={s['id']:s for s in json.loads((root/'data/sources.json').read_text(encoding='utf-8'))}
    rows=[]
    if (root/'data/entries.json').exists():
        for e in json.loads((root/'data/entries.json').read_text(encoding='utf-8')):
            if e['modality']=='visual_only' or e['category']=='typographic_pattern':continue
            for t in [e['term'],*e['aliases']]:
                rows.append([t,'TRUE' if e['context']=='strong_signal' else 'FALSE',e['context'],e['category'],e['id'],','.join(e['languages']),e['context_note'],' '.join(sources[s]['url'] for s in e['source_ids'])])
    else:
        for e in json.loads((root/'data/terms.json').read_text(encoding='utf-8')):
            for language,terms in e['terms'].items():
                for t in terms:rows.append([t,'FALSE','contextual' if e.get('retrieval_enabled',True) else 'research_only',e['category'],e['id'],language,e['context_note'],' '.join(sources[s]['url'] for s in e['source_ids'])])
    headers=['term','enabled','tier','category','entry_id','language','context_note','source_urls']
    # Deduplicate only identical rows; preserve multiple entry/language provenance.
    rows=sorted({tuple(row) for row in rows},key=lambda row:(row[0].casefold(),row[4],row[5],row))
    def tsv(path,headers,rows):
        out=io.StringIO(newline='');w=csv.writer(out,delimiter='\t',lineterminator='\n');w.writerow(headers);w.writerows(rows)
        path.write_text(out.getvalue(),encoding='utf-8-sig',newline='\n')
    tsv(root/'lists/terms_excel.tsv',headers,rows)
    values=sorted({r[0] for r in rows},key=lambda value:(value.casefold(),value))
    (root/'lists/terms_or.txt').write_text(' OR '.join('"'+v.replace('"','\\"')+'"' for v in values)+'\n',encoding='utf-8',newline='\n')
    (root/'lists/terms_pipe.txt').write_text(' | '.join(values)+'\n',encoding='utf-8',newline='\n')
    (root/'lists/terms_readable.txt').write_text('REVIEW VOCABULARY — mentions are not verdicts\n\n'+'\n'.join(f'{r[0]} [{r[2]} / {r[3]}] — {r[7]}' for r in rows)+'\n',encoding='utf-8',newline='\n')
    entities=json.loads((root/'data/canada/lte_entities.json').read_text(encoding='utf-8'))
    assert len({e['id'] for e in entities})==len(entities)
    assert all(e['id'].startswith('ca-'+e['language']+'-') for e in entities)
    registry_rows=[[e['name'],'FALSE','canadian_lte_reference',e['language'],e['id'],e['date_listed'],e['latest_review_raw'],e['aliases_raw'],e['source_url']] for e in entities]
    tsv(root/'lists/canada_lte_excel.tsv',['term','enabled','tier','language','entry_id','date_listed','latest_review_raw','official_aliases_raw','source_url'],registry_rows)
    catalog=['# Canadian Listed Terrorist Entities — source snapshot','','English/French rows are separate localized records, not additional entities. IDs must not be joined across languages. Official aliases are preserved unsplit in JSON/TSV. All names require context.','','| Name | Language | Listed | Source |','| --- | --- | --- | --- |']
    for e in entities:
        name=e['name'].replace('|','\\|')
        catalog.append(f"| {name} | {e['language']} | {e['date_listed']} | [official record]({e['source_url']}) |")
    (root/'CANADA_LTE_CATALOG.md').write_text('\n'.join(catalog)+'\n',encoding='utf-8',newline='\n')
    for language in ['en','fr']:
        values=sorted({e['name'] for e in entities if e['language']==language},key=lambda value:(value.casefold(),value))
        (root/f'lists/canada_lte_{language}_or.txt').write_text(' OR '.join('"'+v.replace('"','\\"')+'"' for v in values)+'\n',encoding='utf-8',newline='\n')
        (root/f'lists/canada_lte_{language}.txt').write_text('\n'.join(values)+'\n',encoding='utf-8',newline='\n')
    print(f'Exported {len(rows)} vocabulary rows and {len(entities)} localized Canadian registry rows')

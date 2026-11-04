"""Literal review-candidate retrieval; no behavior, motive, or risk inference."""
import argparse
import json
import re
import unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def normalize(text):
    text=unicodedata.normalize('NFKC',text).casefold()
    return ' '.join(''.join(c for c in text if unicodedata.category(c)!='Cf').split())

def scan(text,include_contextual=False,include_research=False):
    if not include_contextual:
        return []
    text=normalize(text)
    hits=[]
    for entry in json.loads((ROOT/'data/terms.json').read_text()):
        if not entry.get('retrieval_enabled',True) and not include_research:
            continue
        matched=[]
        for language,terms in entry['terms'].items():
            for term in terms:
                if re.search(r'(?<![^\W_])'+re.escape(normalize(term))+r'(?![^\W_])',text):
                    matched.append({'term':term,'language':language})
        if matched:
            hits.append(dict(id=entry['id'],matched=matched,scope=entry['scope'],
                action='human_review',interpretation='literal_mention_only',source_ids=entry['source_ids']))
    return hits

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('text',nargs='?')
    p.add_argument('--include-contextual',action='store_true',help='Opt into context-dependent review vocabulary; no automatic risk classification')
    p.add_argument('--include-research',action='store_true',help='Also retrieve broad research terms; requires contextual mode')
    a=p.parse_args()
    import sys
    text=a.text if a.text is not None else sys.stdin.read()
    print(json.dumps(dict(mode='literal_retrieval',contextual_enabled=a.include_contextual,
        behavioral_assessment='not_performed',hits=scan(text,a.include_contextual,a.include_research)),ensure_ascii=False,indent=2))

if __name__=='__main__':main()

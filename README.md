# ZERO_NIHL

**Sourced English/German review vocabulary and observation prompts for nihilistic violent extremism (NVE) and related targeted-violence concerns.**

A companion to ZERO_NAZ. This initial collection separates NVE-related networks and exploitation from general attack preparation, prior-attacker emulation, weapons access, and suspicious explosives-related procurement. See [CATALOG.md](CATALOG.md).

## Included

| File | Purpose |
| --- | --- |
| `data/terms.json` | Context-dependent vocabulary, English terms, German translations, provenance |
| `data/indicators.json` | Human observation prompts and evidence questions |
| `data/sources.json` | Exact source links, access limitations, research dates |
| `data/terms.csv`, `data/indicators.csv` | Spreadsheet exports |
| `lists/en_contextual.txt`, `lists/de_contextual.txt` | Opt-in literal retrieval terms |
| `docs/PRINCIPLES.md` | General behavioral review principles |
| `docs/REVIEW.md` | Context, safeguarding, and explosives-related review |

Every record recommends human review. Nothing here diagnoses, predicts violence, infers motive, or establishes network membership. Philosophical nihilism, mental-health conditions, identities, lawful chemistry, ordinary purchases, and historical research are not evidence of NVE. Victim disclosures need support, not automatic punishment.

## Use

Python 3.10+, standard library only:

```sh
python zero_nihl.py --include-contextual "A prevention report about attack planning"
python tools/build.py
python -m unittest discover -s tests -v
```

All vocabulary is ambiguous and requires explicit opt-in. Without `--include-contextual`, the matcher returns no candidates. With it, matches mean only that a literal term appeared. The program never fills in behavioral observation prompts, assigns urgency, counts risk factors, or computes clinical or professional assessment results. A negative match is not a safety assessment.

## Evidence

Sources include FBI, ATF, the UK Home Office, Australian National Security, US Secret Service research, the Combating Terrorism Center at West Point, and public prevention research. `source_attested_label` marks documented names; `project_query_vocabulary` marks project-authored retrieval phrases representing sourced concepts. German variants are project translations, not verified extremist slang. Research dates are not independent expert approval.

General targeted-violence indicators are explicitly scoped separately from NVE. A behavior can warrant safeguarding or threat assessment without proving an extremist motivation. Numeric names and acronyms have unrelated meanings.

Explosives coverage addresses links to intended harm, suspicious transaction context, loss/theft, and access concerns. It does not compile chemical formulas, brand substitutions, ingredient combinations, acquisition sources, quantities, or manufacture instructions. Legitimate industrial, scientific, safety, and journalistic discussion remains context-dependent.

The observation prompts use general behavioral review principles. They are not a validated assessment instrument or a substitute for professional assessment.

Code: MIT. Original dataset annotations: CC0-1.0 to the extent contributors hold the rights. External sources and instruments retain their rights. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Canadian audit and spreadsheet exports

See [Canadian coverage](docs/CANADA.md), [Canadian LTE catalog](CANADA_LTE_CATALOG.md), [audit findings](docs/AUDIT.md), and [Excel usage](docs/EXCEL.md). Read [plain-text terms](lists/terms_readable.txt), import [Excel TSV](lists/terms_excel.tsv), or use [Boolean OR](lists/terms_or.txt) / [pipe-separated](lists/terms_pipe.txt) exports. Context is required for every flag.

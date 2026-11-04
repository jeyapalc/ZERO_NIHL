# Contributing

Maintain `data/terms.json`, `data/indicators.json`, and `data/sources.json`. The seed script is an initial construction record; do not run it over later contributions.

Require exact primary-source links, an original concise annotation, scope, evidence basis, context limitations, and research date. Distinguish source-attested vocabulary from project retrieval phrases and translations. Keep NVE-related evidence separate from general violence-prevention evidence. Sources documenting allegations do not establish guilt or current network status.

Do not add speculative acronyms, identities, diagnoses, generic philosophy, chemistry shopping lists, operational attack details, victim material, or licensed assessment content. Add independent corroboration and expert bilingual review where possible. Record uncertainty and counterevidence.

Regenerate with `python tools/build.py`, run `python -m unittest discover -s tests -v`, and commit exports. Use meaningful false-positive cases for matcher changes. Review source freshness quarterly and after new research. Track additions, corrections, removals, and access limitations in CHANGELOG.md.

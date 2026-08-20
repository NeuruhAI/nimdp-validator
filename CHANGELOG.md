# Changelog

## v1.0.1

- `LICENSE` now carries the complete MIT license text. Earlier tags shipped a truncated file
  that ended mid-sentence with an ellipsis; the same truncation is fixed in
  `nimdp-packs/LICENSE`.
- Replaced `datetime.utcnow()` with a timezone-aware call, which is deprecated from Python 3.12
  and removed in later versions.
- Added a test suite covering keyword matching, phase and token weighting, hard-blocker
  precedence, threshold behaviour, report writing, and the shipped token maps. CI now runs the
  tests on Python 3.11, 3.12, and 3.13 before the sample-specification gate.
- README documents the scoring model, exit codes, the bundled industry packs, the one outbound
  network call, and the limits of keyword-coverage scoring. It previously said no packs shipped
  in this repository while two were present.

## v1.0.0

- Command-line launch-readiness validator with JSON and Markdown reports, external token maps,
  optional Notion output, and a CI gate workflow.

# Changelog

## v1.0.1

### Fixed

- **`LICENSE` was truncated.** The shipped MIT text ended mid-sentence with an ellipsis, 234
  bytes instead of the full grant. The same truncation was present in `nimdp-packs/LICENSE`.
  Both now carry the complete MIT text.
- **Both bundled token packs were invalid YAML.** Unquoted `desc:` and `remediation:` values
  containing a colon made `yaml.safe_load` fail, so `--token-map nimdp-packs/packs/...` never
  worked. All such values are now quoted.
- **`token_map_saas.yaml` was corrupted.** A shell heredoc line from an authoring session had
  been written into the file, truncating the SaaS pack mid-token and appending a second,
  unrelated token pack. The stray heredoc and the appended pack are removed. The partial
  trailing `ROCKS` token was dropped rather than reconstructed, since its remaining fields were
  never present to recover.
- **`load_token_map` failed silently.** A requested token map that could not be read — missing
  file, PyYAML not installed, unparseable YAML — was replaced by the built-in map with no
  message, scoring the input against a different rubric than the one asked for. Every such case
  is now an error and exits `2`. `--token-map` no longer defaults to a filename; `./token_map.yaml`
  is used when present and no map was requested.
- **`datetime.utcnow()`** is deprecated from Python 3.12 and slated for removal. Replaced with
  `datetime.now(timezone.utc)` in both call sites.
- **`requests` pinned to a version with an open advisory.** Bumped `requests` from 2.32.4 to
  2.33.0, which patches insecure temporary-file reuse in `extract_zipped_paths()`.
- **README contradicted the repository.** It stated that no domain-specific packs shipped here
  while two were present.

### Added

- A test suite: keyword matching, phase and token weighting, hard-blocker precedence over the
  numeric score, threshold boundaries, report writing, token-map loading failures, and
  structural checks on every shipped pack — including that each pack can actually reach its own
  pass threshold, and that no pack contains shell fragments.
- CI runs the tests on Python 3.11, 3.12 and 3.13 before the sample-specification gate.
- README documents the scoring model, the exit codes, the bundled packs, and the single
  outbound network call.

### Note for maintainers

Phase weights do not sum to 1.0 in the bundled packs: `token_map_defense.yaml` sums to 1.02 and
`token_map_saas.yaml` to 0.97. Both remain able to reach their own pass thresholds, so this is
recorded rather than silently rewritten — changing rubric weights is an authoring decision.

## v1.0.0

- Command-line launch-readiness validator with JSON and Markdown reports, external token maps,
  optional Notion output, and a CI gate workflow.

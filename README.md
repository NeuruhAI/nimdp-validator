# NIMDP Validator

[![NIMDP Gate](https://github.com/NeuruhAI/nimdp-validator/actions/workflows/validate.yml/badge.svg)](https://github.com/NeuruhAI/nimdp-validator/actions/workflows/validate.yml)

A command-line launch-readiness validator for product, marketing, sales, and operations specifications.

The validator reads one or more Markdown specifications, scores them against a token map, and writes a JSON and Markdown report. It can be run locally or wired in as a CI gate.

## Install

```bash
git clone https://github.com/NeuruhAI/nimdp-validator.git
cd nimdp-validator
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Requires Python 3.11 or newer.

## Sixty-second example

```bash
python validator.py \
  --project-name "Demo" \
  --input samples/demo_spec.md \
  --outdir reports
```

Expected output:

```text
=== NIMDP VALIDATION SUMMARY ===
Project: Demo
Status:  MARKET READY
Score:   92.5% (threshold 80.0%)
Hard Block Triggered: False
Reports: reports/<timestamp>__Demo.json
         reports/<timestamp>__Demo.md
```

Or use the Make target, which creates the virtual environment for you:

```bash
make validate
```

## How scoring works

A token map declares phases, each with a weight, and tokens within each phase, each with its
own weight, a keyword list, and a remediation string. A token scores if any of its keywords
appears in the joined input text, matched case-insensitively as a substring. Phase scores are
weight-normalised within the phase, then multiplied by the phase weight and summed.

A token marked `hard_blocker` that does not score sets `BLOCKED`, which overrides the numeric
score unless the token map sets `hard_block_on_fail: false`.

## Exit codes

| Code | Status | Meaning |
| --- | --- | --- |
| `0` | `MARKET READY` | Score at or above the threshold, no hard blocker missing. |
| `1` | `NOT READY` | Score below the threshold. |
| `2` | — | Inputs unreadable, or the requested token map is missing, unparseable, or has no `phases`. |
| `3` | `BLOCKED` | A hard-blocker token is missing. |

The nonzero codes are what make this usable as a CI gate.

## Token maps

The default token map is [`token_map.yaml`](token_map.yaml). Point at a different one with
`--token-map`:

```bash
python validator.py \
  --project-name "Demo" \
  --input samples/demo_spec.md \
  --outdir reports \
  --token-map nimdp-packs/packs/token_map_saas.yaml
```

Two industry packs ship in [`nimdp-packs/packs/`](nimdp-packs/packs): `token_map_saas.yaml`
and `token_map_defense.yaml`. They contain scoring vocabulary and weights only — no customer
data, no credentials, no endpoints. Other internal packs are not published here.

If a token map is requested and cannot be honoured — missing file, PyYAML not installed,
unparseable YAML, or no `phases` mapping — the validator exits `2` rather than scoring against
the built-in map. Only a run that requests no map at all uses the built-in one.

## Optional Notion output

`--push-notion` posts the summary to a Notion database. It reads two environment variables and
is a no-op unless you set them:

```bash
export NOTION_API_KEY="..."
export NOTION_DATABASE_ID="..."

python validator.py \
  --project-name "Demo" \
  --input samples/demo_spec.md \
  --outdir reports \
  --push-notion
```

This is the only outbound network call the tool makes. Without `--push-notion` the validator
reads and writes local files only.

## Build a standalone executable

```bash
make package
```

This installs PyInstaller into the project virtual environment and writes the executable under
`dist/`.

## Test

```bash
python -m unittest discover -s tests -v
```

## Safety boundary

The validator checks whether a specification mentions the things a token map says it should. It
is a keyword-coverage gate, not a judgement about whether a plan is good, correct, or true: a
document can score 100% and still be wrong. Treat `MARKET READY` as "the required topics are
covered", nothing more.

Keyword matching is plain case-insensitive substring matching, so a keyword can match inside a
larger word, and a token can score on a passing mention or a negation.

## License

MIT. See [`LICENSE`](LICENSE).

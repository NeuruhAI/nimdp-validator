VENV = .venv
PY = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

.PHONY: venv validate package clean backup run-local open validate-local last diff

venv:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt || true

## Default validate: CI-style sample run (venv)
validate: venv
	mkdir -p reports
	$(PY) validator.py --project-name "Local" --input samples/demo_spec.md --outdir reports

## Local token_map.yaml workflow (kept from history; avoids clobbering validate)
backup:
	cp -f token_map.yaml "token_map.$(shell date +%Y%m%d-%H%M%S).yaml.bak"

run-local:
	mkdir -p out
	python3 validator.py --project-name valuator --input token_map.yaml --outdir out

validate-local: backup run-local open

open:
	@latest=$$(ls -t out/*__valuator.md 2>/dev/null | head -n1); \
	if [ -n "$$latest" ]; then echo "Opening $$latest"; open "$$latest"; else echo "No out/__valuator.md"; fi

last:
	@ls -lt out/*__valuator.* 2>/dev/null | head -n4

package: venv
	$(PIP) install pyinstaller
	$(VENV)/bin/pyinstaller --onefile validator.py

clean:
	rm -rf out reports dist build *.spec

diff:
	@latest=$$(ls -t token_map.*.yaml.bak 2>/dev/null | head -n1); \
	if [ -n "$$latest" ]; then echo "Comparing token_map.yaml ↔ $$latest"; diff -u "$$latest" token_map.yaml || true; else echo "No backups"; fi

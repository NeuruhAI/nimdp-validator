VENV=.venv
PY=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

.PHONY: venv validate package clean

venv:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt || true

validate: venv
	mkdir -p reports
	$(PY) validator.py --project-name "Local" --input samples/demo_spec.md --outdir reports

package: venv
	$(PIP) install pyinstaller
	$(VENV)/bin/pyinstaller --onefile validator.py

clean:
	rm -rf $(VENV) build dist *.spec reports

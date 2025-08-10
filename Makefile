.PHONY: validate backup run open last clean diff

# 1-step: backup current YAML, run validator, and show output path
validate: backup run open

# Backup with timestamp (.bak lives beside token_map.yaml)
backup:
	cp -f token_map.yaml "token_map.$(shell date +%Y%m%d-%H%M%S).yaml.bak"

# Run the validator
run:
	python3 validator.py --project-name valuator --input token_map.yaml --outdir out

# Open the newest MD report (macOS)
open:
	@latest=$$(ls -t out/*__valuator.md | head -n1); \
	echo "Opening $$latest"; \
	open "$$latest"

# Show the newest run file pair
last:
	@ls -lt out/*__valuator.* | head -n4

# Clean out reports
clean:
	rm -rf out

# See what changed vs last backup (requires 'diff')
diff:
	@latest=$$(ls -t token_map.*.yaml.bak | head -n1); \
	echo "Comparing token_map.yaml ↔ $$latest"; \
	diff -u "$$latest" token_map.yaml || true

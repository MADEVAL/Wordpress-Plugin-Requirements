.PHONY: check validate test install-dry

check: validate test install-dry

validate:
	python tests/validate_skill.py

test:
	python -m unittest discover -s tests -p "test_*.py"

install-dry:
	python install.py --target project --dry-run

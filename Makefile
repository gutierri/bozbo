qa-code:
	flake8 bozbo.py tests.py

test:
	python tests.py

.PHONY: test qa-code

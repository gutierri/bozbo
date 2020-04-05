all: test

init:
	pip install -r requirements-dev.txt
	pip install -e .

qa-code:
	flake8 bozbo.py tests.py

test:
	python -m unittest tests.py


.PHONY: test qa-code init all

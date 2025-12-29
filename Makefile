SHELL := /bin/bash

.PHONY: regression lint check

regression:
	python -m pytest harness/tests -v

lint:
	python -m py_compile hooks/*.py

check: lint regression

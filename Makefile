.PHONY: install-dependencies isort black flake8

install-dependencies:
	python -m pip install --upgrade pip
	pip install isort black flake8

isort:
	isort --skip venv --skip tesseract --skip "auth compiled" .

black:
	black --check --diff --exclude venv --exclude tesseract --exclude "auth compiled" .

flake8:
	flake8 --exclude=venv,tesseract,"auth compiled" .

test: isort black flake8

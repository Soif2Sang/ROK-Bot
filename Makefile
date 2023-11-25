.PHONY: install-dependencies isort black flake8

install-dependencies:
	python -m pip install --upgrade pip
	pip install isort black flake8

isort:
	isort --skip venv --skip tesseract --skip "auth compiled" --skip "utils/Crypto" .

black:
	black --check --diff --exclude venv --exclude tesseract --exclude "auth compiled" --exclude "utils/Crypto".

flake8:
	flake8 --exclude=venv,tesseract,"auth compiled","utils/Crypto" .

test: isort black flake8

.PHONY: install-dependencies isort black flake8

install-dependencies:
	python -m pip install --upgrade pip
	pip install isort black flake8

isort:
	isort --skip venv --skip tesseract --skip "auth compiled" --skip "utils/Crypto" --skip "*__pycache__*" .

test: isort

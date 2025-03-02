test:
	pytest

serve:
	fastapi dev

venv:
	source venv/bin/activate

deps:
	pip install -r requirements.txt

initial:
	python3 -m venv venv

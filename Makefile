test:
	pytest

serve:
	fastapi dev

deps:
	source venv/bin/activate
	pip install -r requirements.txt

initial:
	brew install python3
	python3 -m venv venv


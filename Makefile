install:
	pip install -r requirements.dev.txt

run: 
	uvicorn api.main:app --reload

format:
	black .

lint:
	black . --check
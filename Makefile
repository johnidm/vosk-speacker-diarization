
model:
	wget https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip -P /tmp
	unzip -o /tmp/vosk-model-small-pt-0.3.zip -d ./model

install:
	pip install -r requirements.dev.txt

run: 
	uvicorn api.main:app --reload

format:
	black .

lint:
	black . --check
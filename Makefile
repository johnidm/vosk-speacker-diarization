
IMAGE_NAME=vosk-speacker-diarization:latest

model:
	@wget https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip -P /tmp
	@unzip -o /tmp/vosk-model-small-pt-0.3.zip -d ./model

install:
	@pip install -r requirements.dev.txt

run: 
	@uvicorn api.main:app --reload

format:
	@black .

lint:
	@black . --check

docker-build:
	@docker build -t $(IMAGE_NAME) .

docker-rm:
	@docker rm -f $(IMAGE_NAME)

docker-run: docker-build
	@docker container run --name vosk-speacker-diarization -i -t -p 8000:8000  --rm $(IMAGE_NAME)

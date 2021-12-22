from fastapi import FastAPI
from vosk import KaldiRecognizer, Model
from pydub import AudioSegment
import json
from vosk import KaldiRecognizer, Model
from urllib.request import urlretrieve
from starlette.status import HTTP_201_CREATED
import logging
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import os


app = FastAPI()


SAMPLE_RATE = 16000
MODEL_DIR = os.path.join(os.getcwd(), "model/vosk-model-small-pt-0.3")

CHUNK_SIZE = 10 * 1000  # ms

model = Model(MODEL_DIR)


@app.get("/")
async def home():
    return {"status": "Running", "model_dir": MODEL_DIR, "sample_rate": SAMPLE_RATE}


class TranscribeBody(BaseModel):
    url: str


class TranscriptionDone(BaseModel):
    text: str


@app.post("/transcribe", response_model=TranscriptionDone)
async def transcribe(body: TranscribeBody):
    url = body.url

    print(f"Downlaoding url: {url}")
    file, _ = urlretrieve(url)

    print(f"Converting audio: {file}")
    audio = AudioSegment.from_file(file)
    audio = audio.set_frame_rate(SAMPLE_RATE)
    audio = audio.set_channels(1)

    rec = KaldiRecognizer(model, SAMPLE_RATE)
    rec.SetWords(True)

    for index, chunk in enumerate(audio[::CHUNK_SIZE]):
        data = chunk.get_array_of_samples().tobytes()
        rec.AcceptWaveform(data)
        print(f"Transcription chunk: {index + 1}")

    print("Transcription done")
    transcription = json.loads(rec.FinalResult())

    return JSONResponse(
        status_code=HTTP_201_CREATED, content={"text": transcription["text"]}
    )

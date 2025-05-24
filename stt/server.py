from fastapi import FastAPI
import sounddevice as sd
import asyncio
import threading

from dweller_stt import DwellerSTT

import sounddevice as sd

print(sd.query_devices())

app = FastAPI()

stt = DwellerSTT(
    device=1,
    samplerate=16000,
    model_path="./models/vosk-model-en-us-0.22"
)
stt.loop.create_task(stt.transcribe())

@app.get("/listen")
async def root():
    await asyncio.to_thread(stt.listen)



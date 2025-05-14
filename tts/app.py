import numpy as np
import sounddevice as sd
import asyncio
from fastapi import FastAPI, Request
from pydantic import BaseModel
from kokoro_onnx import Kokoro

app = FastAPI()

# Load Kokoro and voices at startup
kokoro = Kokoro("model/kokoro-v1.0.onnx", "voices-v1.0.bin")
alpha = kokoro.get_voice_style("jf_alpha")
tebukuro = kokoro.get_voice_style("jf_tebukuro")
blend = alpha * 0.25 + tebukuro * 0.75

class SpeechRequest(BaseModel):
    text: str

@app.post("/speak")
async def speak(req: SpeechRequest):
    stream = kokoro.create_stream(
        req.text,
        voice=blend,
        speed=1.15,
        lang="en-us",
    )

    async def play():
        async for samples, sample_rate in stream:
            sd.play(samples, sample_rate)
            sd.wait()

    # Run playback as a coroutine
    asyncio.create_task(play())

    return {"status": "Speaking started"}

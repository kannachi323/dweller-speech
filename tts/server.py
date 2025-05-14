
import sounddevice as sd
import asyncio
import yaml
from fastapi import FastAPI, Request


from dweller_tts import DwellerTTS
from kokoro_onnx import Kokoro


with open("openapi.yaml", "r") as f:
    openapi_spec = yaml.safe_load(f)


app = FastAPI()
app.openapi_schema = openapi_spec

tts = DwellerTTS(
    model_path="model/kokoro-v1.0.onnx",
    voices_path="voices-v1.0.bin",
    voice_styles = {"jf_alpha": 0.7, "af_heart": 0.3}
)

@app.post("/talk")
async def talk(req: dict):
    tts.generate_voice_stream(req.get("text", ""), req.get("speed", 1.5))

    if tts.stream is not None:
        asyncio.create_task(tts.talk())

        return {"status": "Speaking started"}

    else:
        return {"status": "No message provided"}



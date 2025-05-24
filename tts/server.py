
import sounddevice as sd
import asyncio
import yaml
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect


from dweller_tts import DwellerTTS
from kokoro_onnx import Kokoro


with open("openapi.yaml", "r") as f:
    openapi_spec = yaml.safe_load(f)


app = FastAPI()
app.openapi_schema = openapi_spec

tts = DwellerTTS(
    model_path="models/kokoro-v1.0.onnx",
    voices_path="models/voices-v1.0.bin",
    voice_styles = [("jf_alpha", 0.7), ("af_heart", 0.3)]
)

@app.websocket("/talk")
async def talk(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()
            text = data.get("text", "")
            speed = data.get("speed", 1.15)

            if not text:
                await websocket.send_json({"status": "No text provided"})
                continue

            tts.generate_voice_stream(text, speed)

            if tts.stream is not None:
                asyncio.create_task(tts.talk())
                await websocket.send_json({"status": "Speaking started"})

            else:
                return {"status": "No message provided"}
    except WebSocketDisconnect:
        print("WebSocket disconnected")


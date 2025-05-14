import numpy as np
import soundfile as sf
import sounddevice as sd

from kokoro_onnx import Kokoro

import sounddevice as sd

from kokoro_onnx import Kokoro

class DwellerTTS():
    def __init__(self, model_path, voices_path, voice_styles):
        self.model_path = model_path
        self.voices_path = voices_path
        self.kokoro = Kokoro(model_path, voices_path)
        self.voice = self.create_voice(voice_styles)
       
        self.stream = None
    
    def create_voice(self, voice_styles):
        if sum(voice_styles.values()) != 1:
            raise Exception("Weights must add up to 1")
        
        voice = np.zeros_like(np.array(self.kokoro.get_voice_style(list(voice_styles.keys())[0])))

        for vs, wt in voice_styles.items():
            voice += self.kokoro.get_voice_style(vs) * wt
    
        
        return voice


    def generate_voice_stream(self, input_text: str = "", speed: float = 1.5):
        self.stream = self.kokoro.create_stream(
            input_text,
            voice=self.voice,
            speed=speed,
            lang="en-us",
        )
        
    async def talk(self):
        async for samples, sample_rate in self.stream:
            sd.play(samples, sample_rate)
            sd.wait()
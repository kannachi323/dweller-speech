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
        self.voices = self.create_voices(voice_styles)
        self.dweller_voice = self.create_dweller_voice(voice_styles)
       
        self.stream = None
    
    def create_voices(self, voice_styles):
        voices = {}
        total_weight = 0
        for vs, weight in voice_styles:
            voices[vs] = weight
            total_weight += weight
        
        if total_weight != 1:
            raise Exception("Weights must add up to 1")
        
        return voices
    
    def create_dweller_voice(self, voice_styles):
        
        dweller_voice = np.full((510, 1, 256), 0.0, dtype=np.float32)

        for vs, wt in voice_styles:
            dweller_voice += self.kokoro.get_voice_style(vs) * wt
    
        
        return dweller_voice


    def generate_voice_stream(self, input_text: str = "", speed: float = 1.15):
        self.stream = self.kokoro.create_stream(
            input_text,
            voice=self.dweller_voice,
            speed=speed,
            lang="en-us",
        )
        
    async def talk(self):
        async for samples, sample_rate in self.stream:
            sd.play(samples, sample_rate)
            sd.wait()
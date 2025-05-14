from kokoro import KPipeline

import torch

from IPython.display import display, Audio
import sounddevice as sd
import soundfile as sf
import io

pipeline = KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M', device="mps")

text = '''
Hi! My name is Dweller. I am virtual AI assistant. Please let me know how I can help you.
'''
furina_voice ='tensors/furina_embedding.pt'

af_heart = torch.load("voices")

generator = pipeline(text=text, voice="af_heart")

for i, (gs, ps, audio) in enumerate(generator):
    print(i, gs, ps)
    sd.play(audio, samplerate=24000)
    sd.wait()
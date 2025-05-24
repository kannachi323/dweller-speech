
import asyncio
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer


class DwellerSTT:
    def __init__(self, device, samplerate, model_path):
        self.filename = None
        self.device = device
        self.samplerate = samplerate
        self.model = Model(model_path=model_path)
        self.audio_buffer = queue.Queue()
        self.output_buffer = asyncio.Queue()
        self.loop = asyncio.get_event_loop()
        self.listen = False

    def callback(self, indata, frames, time, status):
        self.audio_buffer.put(bytes(indata))


    def listen(self):
        try:
            with sd.RawInputStream(samplerate=self.samplerate, blocksize=8000, 
                device=self.device, dtype="int16", channels=1, callback=self.callback):

                rec = KaldiRecognizer(self.model, self.samplerate)

                print("listening...")
                self.listen = True
                while self.listen:
                    if rec.AcceptWaveform(self.audio_buffer.get()): #kalid rec knows when user stops talking, no audio input
                        self.output_buffer.put(rec.Result())
                        
                        asyncio.run_coroutine_threadsafe(self.output_buffer.put(rec.Result()), self.loop)
 
        except KeyboardInterrupt:
            print("\nStopped by user.")
        except Exception:
            print("uh oh, something went wrong with dweller-stt")
    
    async def transcribe(self):
        try:
            while True:
                result = await self.output_buffer.get()
                print(result, flush=True)
                self.listen = False
                
        except asyncio.CancelledError:
            print("Transcription stopped.")
           
                

    def format_data(self, text_input):
        static_memory = """
        You are Dweller, a helpful and slightly witty AI assistant.
        You live inside a local personal computer environment.
        You were created to assist with coding, system control, and casual conversation.
        You exist in 2025.
        You are a voice interface that responds to live speech inputs.

        Please respond only to the last message in the conversation. Keep responses short and concise."""
        
        return f"{static_memory}\n\nconversation: {"\n".join(self.data)}\n\nlast_message: {text_input}\n\nreply"
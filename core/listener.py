import os
import subprocess
import time
from groq import Groq

class VoiceListener:
    def __init__(self, groq_api_key=None):
        self.api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key)
        self.audio_file = "input.wav"

    def record_voice(self, duration=4):
        print(f"\n[Listening...] {duration} seconds...")
        # Termux mic se raw WAV record karna
        os.system(f"termux-microphone-record -d -f {self.audio_file} -l {duration}")
        time.sleep(duration + 0.5)
        os.system("termux-microphone-record -q")

    def transcribe(self):
        if not os.path.exists(self.audio_file):
            return ""
        
        try:
            with open(self.audio_file, "rb") as file:
                transcription = self.client.audio.transcriptions.create(
                    file=(self.audio_file, file.read()),
                    model="whisper-large-v3-turbo",
                    response_format="text",
                    language="hi"  # Hindi, Marathi aur English mixed recognize karega
                )
            os.remove(self.audio_file)
            return transcription.strip()
        except Exception as e:
            print(f"[STT Error]: {e}")
            return ""

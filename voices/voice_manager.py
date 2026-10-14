import json
import os
import asyncio
import edge_tts

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "profiles.json")

class VoiceEngine:
    def __init__(self):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            self.config = json.load(f)
        self.current_persona = self.config.get("active_persona", "Jiny")

    def set_persona(self, name):
        if name in self.config["personas"]:
            self.current_persona = name
            print(f"[Voice] Persona switched to: {name}")
        else:
            print(f"[Voice] Persona '{name}' not found.")

    async def speak(self, text, output_file="output.mp3"):
        persona_data = self.config["personas"][self.current_persona]
        voice = persona_data["edge_voice"]

        print(f"[{self.current_persona} speaking ({persona_data['language']})]: {text}")
        
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        
        # Audio playback on Android/Termux
        os.system(f"mpv {output_file} > /dev/null 2>&1 || play {output_file} > /dev/null 2>&1")

if __name__ == "__main__":
    engine = VoiceEngine()
    
    # Test 1: Jiny (Hindi)
    asyncio.run(engine.speak("नमस्ते! मैं जिनी हूँ। AI-OS तैयार है।"))
    
    # Test 2: Shri (Marathi)
    engine.set_persona("Shri")
    asyncio.run(engine.speak("नमस्कार! मी श्री आहे. तुमचं काम सांगा."))

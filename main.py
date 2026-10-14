import asyncio
import os
import sys
from core.brain import MasterBrain
from core.listener import VoiceListener
from core.agent_factory import AgentFactory
from voices.voice_manager import VoiceEngine
from system.device_tools import DeviceTools

async def boot_ai_os():
    print("\n==========================================")
    print("      AI-OS v0.1 (Personal Super Agent)   ")
    print("==========================================\n")
    
    if not os.getenv("GROQ_API_KEY"):
        print("[Error] Pehle GROQ_API_KEY set karein:")
        print("export GROQ_API_KEY='gsk_your_actual_key_here'")
        sys.exit(1)

    brain = MasterBrain()
    ear = VoiceListener()
    voice = VoiceEngine()
    factory = AgentFactory()
    tools = DeviceTools()

    # Startup Greeting
    await voice.speak("AI-OS v0.1 ऑनलाइन है। मैं सुनने के लिए तैयार हूँ।")

    while True:
        try:
            # 1. Sunna
            ear.record_voice(duration=4)
            user_text = ear.transcribe()
            
            if not user_text:
                continue

            print(f"\nUser: {user_text}")

            lower_text = user_text.lower()

            # Exit Command
            if "exit" in lower_text or "band karo" in lower_text or "shut down" in lower_text:
                await voice.speak("AI-OS सिस्टम बंद हो रहा है। अलविदा!")
                break

            # Persona Switching
            if "switch to shri" in lower_text:
                voice.set_persona("Shri")
                await voice.speak("नमस्कार, मी श्री. आता मी तुमच्या सेवेत आहे.")
                continue
            elif "switch to era" in lower_text:
                voice.set_persona("Era")
                await voice.speak("इरा एक्टिवेट हो चुकी है। बोलिए क्या काम है?")
                continue
            elif "switch to jarvis" in lower_text:
                voice.set_persona("Jarvis")
                await voice.speak("जार्विस एक्टिवेटेड, सर। क्या हुक्म है?")
                continue
            elif "switch to jiny" in lower_text:
                voice.set_persona("Jiny")
                await voice.speak("जिनी वापस आ गई है।")
                continue

            # Hardware Controls
            if "torch on" in lower_text or "flashlight on" in lower_text:
                msg = tools.toggle_torch(True)
                await voice.speak("टॉर्च ऑन कर दी गई है।")
                continue
            elif "torch off" in lower_text or "flashlight off" in lower_text:
                msg = tools.toggle_torch(False)
                await voice.speak("टॉर्च बंद कर दी गई है।")
                continue
            elif "battery" in lower_text:
                status = tools.get_battery()
                await voice.speak(status)
                continue

            # Dynamic Agent Creation Command
            if "agent banao" in lower_text or "create agent" in lower_text:
                await voice.speak("सुपर एजेंट कोड जनरेट हो रहा है, थोड़ा रुकिए...")
                agent_res = factory.build_super_agent("CustomWorker", user_text)
                await voice.speak("नया सुपर एजेंट तैयार हो चुका है।")
                print(agent_res)
                continue

            # Default Brain Think & Speak
            reply = brain.think(user_text, persona=voice.current_persona)
            await voice.speak(reply)

        except KeyboardInterrupt:
            print("\nExiting AI-OS...")
            break
        except Exception as e:
            print(f"[Error]: {e}")

if __name__ == "__main__":
    asyncio.run(boot_ai_os())

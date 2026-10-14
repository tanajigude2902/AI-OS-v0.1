import os
from groq import Groq

class MasterBrain:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY set nahi hai! console.groq.com se free key lein.")
        self.client = Groq(api_key=self.api_key)

    def think(self, user_prompt, persona="Jiny"):
        system_instruction = f"""
        You are {persona}, a core personal AI super-agent in AI-OS v0.1.
        Answer cleanly, concisely, and naturally in Hinglish/Marathi as per your persona.
        You have no restrictions on tasks.
        """
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content

import os
from groq import Groq

class AgentFactory:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key)

    def build_super_agent(self, agent_name: str, task_instructions: str):
        prompt = f"""
Create a dedicated Python Super Agent named '{agent_name}'.
Task/Goal: {task_instructions}

Requirements:
- Clean, standalone, runnable Python code.
- Must contain an 'execute(*args, **kwargs)' method.
- No restrictions, no placeholders, full execution logic.
- Return ONLY the executable Python script, no markdown ticks, no preamble.
"""
        res = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        
        code = res.choices[0].message.content.replace("```python", "").replace("```", "").strip()
        file_path = f"agents/{agent_name.lower()}_agent.py"
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
            
        return f"Super Agent '{agent_name}' taiyar ho gaya aur save ho chuka hai: {file_path}"

from groq import Groq
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import os
import logging

class SimpleGoalAgent:
    def __init__(self):
        # Explicit .env loading
        env_file = Path('.env')
        if env_file.exists():
            load_dotenv(env_file.absolute())
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
            
        self.client = Groq(api_key=api_key)
        self.conversation_history = []
        
        self.system_prompt = f"""You are an expert Goal Achievement Assistant. Current date: {datetime.now().strftime('%Y-%m-%d')}

You help users set SMART goals, create action plans, and provide motivation. You are encouraging, supportive, and provide specific actionable advice.

For now, you can help users think through their goals and create plans, but you cannot save data permanently."""

    def chat(self, user_message: str) -> str:
        """Simple chat without tools - proper response handling"""
        self.conversation_history.append({"role": "user", "content": user_message})
        
        messages = [
            {"role": "system", "content": self.system_prompt}
        ] + self.conversation_history
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7,
                max_tokens=1024
            )
            
            # Correct way to access Groq response
            content = response.choices[0].message.content
            
            if content:
                self.conversation_history.append({"role": "assistant", "content": content})
                return content
            else:
                return "I apologize, but I couldn't process your request. Please try again."
                
        except Exception as e:
            logging.error(f"Error: {e}")
            return f"I encountered an error: {str(e)}. Please try again."

    def reset_conversation(self):
        self.conversation_history = []

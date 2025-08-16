import os
from pathlib import Path
from dotenv import load_dotenv

# Explicit .env loading - fixes Windows PowerShell issues
env_file = Path(__file__).parent / '.env'
if env_file.exists():
    load_dotenv(env_file.absolute())

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DB_NAME = os.getenv("DB_NAME", "goal_agent")
    
    # Debug output
    if not GROQ_API_KEY:
        print("❌ WARNING: GROQ_API_KEY not found in environment variables")
    
    # Groq model configurations
    MODELS = {
        "primary": "llama-3.3-70b-versatile",
        "fast": "llama-3.1-8b-instant", 
        "creative": "mixtral-8x7b-32768"
    }
    
    # Generation parameters
    GENERATION_PARAMS = {
        "temperature": 0.7,
        "max_tokens": 4096,
        "top_p": 0.9
    }

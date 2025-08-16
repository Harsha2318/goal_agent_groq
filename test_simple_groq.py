from groq import Groq
import os
from pathlib import Path
from dotenv import load_dotenv

def test_groq():
    # Explicit .env loading
    env_file = Path('.env')
    if env_file.exists():
        load_dotenv(env_file.absolute())
        print(f"✅ Loaded .env from: {env_file.absolute()}")
    else:
        print(f"❌ .env file not found at: {env_file.absolute()}")
    
    # Check if API key is loaded
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not found in environment")
        return False
    
    print(f"✅ Found GROQ_API_KEY: {api_key[:10]}...")
    
    try:
        client = Groq(api_key=api_key)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Say hello in one sentence"}],
            max_tokens=50
        )
        
        content = response.choices[0].message.content
        print("✅ Success! Response:", content)
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_groq()

import os
from google import genai
from google.genai import types

def test_search():
    # Attempt to read api key from .env or config
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("No GEMINI_API_KEY in environment")
        return
        
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.5-pro',
        contents='Find 5 TikTok video URLs about "flame humidifier review". Just return the URLs as a list.',
        config=types.GenerateContentConfig(
            tools=[{"google_search": {}}],
            temperature=0.2
        )
    )
    print(response.text)

test_search()

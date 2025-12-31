import os
import asyncio
from typing import AsyncGenerator

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GENIMI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GENIMI_API_KEY:
    raise RuntimeError("Gemini API key not set in environment variables")

genai.configure(api_key=GENIMI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

async def stream_llm_response(prompt: str) -> AsyncGenerator[str, None]:
    """Simulates streaming llm response"""

    response = model.generate_content(prompt, stream=True)

    for chunk in response:
        if not chunk.text:
            continue
            
        yield chunk.text
        await asyncio.sleep(0)
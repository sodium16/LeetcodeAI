import asyncio
import os

from dotenv import load_dotenv
from fastapi import HTTPException, APIRouter
from openai import OpenAI

from .base import AIProvider

router = APIRouter()

# Global tracking variable to lock execution per endpoint context
is_processing_generation = False

load_dotenv()


class OpenAIProvider(AIProvider):

    def __init__(self):

        api_key = os.getenv("OPENAI_API_KEY")


        if not api_key:
            raise Exception("OPENAI_API_KEY missing")

        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt: str) -> str:

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()


@router.post("/generate-blog")
async def generate_blog(payload: dict):
    global is_processing_generation
    
    # Check if a request is already running inside the AI loop
    if is_processing_generation:
        raise HTTPException(
            status_code=429, 
            detail="A blog generation request is already in progress. Please wait."
        )
        
    try:
        # Acquire lock
        is_processing_generation = True
        
        # --- Existing AI Generation Logic Here ---
        # result = await call_llm_provider(payload)
        await asyncio.sleep(2) # Simulating AI processing delay
        
        return {"status": "success", "message": "Blog created successfully"}
        
    finally:
        # Release the lock safely even if the LLM crashes or times out
        is_processing_generation = False

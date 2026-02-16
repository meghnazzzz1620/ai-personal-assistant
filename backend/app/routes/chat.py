from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import requests
import json

from app.auth import get_current_user
from app.database import get_db
from app.models.conversation import Conversation
from app.services.memory_service import search_memory

router = APIRouter(prefix="/chat", tags=["Chat"])

OLLAMA_URL = "http://ollama:11434/api/generate"

@router.post("/")
def chat(message: str,
         db: Session = Depends(get_db),
         current_user = Depends(get_current_user)):

    memory_context = search_memory(db, current_user.id, message)

    prompt = f"""
You are a personalized AI assistant.

User memory:
{memory_context}

User message:
{message}

Answer conversationally and clearly.
"""

    def generate():
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "phi3",
                "prompt": prompt,
                "stream": True
            },
            stream=True
        )

        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    yield data["response"]

    return StreamingResponse(generate(), media_type="text/plain")

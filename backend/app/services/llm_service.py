import requests

def generate_response(context: str, user_query: str):

    prompt = f"""
You are a personalized AI assistant.
Be concise. Keep answers short unless user asks for detail.

Context:
{context}

User Question:
{user_query}

Guidelines:
- Use structured memory if available.
- Answer clearly and briefly.
"""

    response = requests.post(
        "http://ollama:11434/api/generate",
        json={
            "model": "phi3",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 150
            }
        }
    )

    return response.json()["response"]

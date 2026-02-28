"""Wrapper around OpenAI API with simple safety and structured response parsing."""
import json
import openai
from typing import Dict, Any
from app.config import settings

openai.api_key = settings.OPENAI_API_KEY


def call_chat(prompt_system: str, prompt_user: str, max_tokens: int = 600) -> Dict[str, Any]:
    """Call the OpenAI ChatCompletion endpoint and return parsed JSON.

    The assistant is instructed to respond with JSON. We attempt to parse it safely.
    """
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt_system},
                {"role": "user", "content": prompt_user},
            ],
            temperature=0.2,
            max_tokens=max_tokens,
        )
        content = resp["choices"][0]["message"]["content"]
        # Attempt to extract JSON object from the content
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1:
            json_text = content[start:end+1]
            try:
                return json.loads(json_text)
            except Exception:
                # fallback: try to return raw content
                return {"raw": content}
        return {"raw": content}
    except Exception as e:
        return {"error": str(e)}

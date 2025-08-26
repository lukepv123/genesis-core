import os
from typing import Optional
try:
    import httpx
except Exception:  # pragma: no cover
    httpx = None

class LLMClient:
    def __init__(self, provider: str, model: str, api_key_env: str):
        self.provider = provider
        self.model = model
        self.api_key = os.getenv(api_key_env, "")

    def complete(self, prompt: str, user_text: str, model: Optional[str] = None) -> str:
        if not httpx or not self.api_key:
            return f"[LLM OFFLINE] {prompt.strip()} | User: {user_text}"
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": model or self.model,
                "messages": [
                    {"role": "system", "content": prompt or ""},
                    {"role": "user", "content": user_text},
                ],
            }
            with httpx.Client(timeout=30) as client:
                resp = client.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[LLM ERROR] {e}"

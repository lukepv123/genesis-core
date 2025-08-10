import requests

class OpenRouterGPTFreeClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        # Modelo gratuito do OpenRouter
        self.model = "openai/gpt-oss-20b:free"
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def get_chat_response(self, messages: list) -> str:
        try:
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={"model": self.model, "messages": messages}
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception:
            return "Please confirm the key token of your AI server!"

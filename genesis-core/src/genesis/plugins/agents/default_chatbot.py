from typing import Dict, Any
from ...core.base_agent import BaseAgent
from ...core.registry import register_agent

@register_agent
class DefaultChatbot(BaseAgent):
    name = "default_chatbot"

    def handle(self, text: str, context: Dict[str, Any]) -> str:
        llm = self.services.get("llm")
        system_prompt = self.prompts.get(self.config.get("system_prompt_ref", "default"), "")
        return llm.complete(prompt=system_prompt, user_text=text)

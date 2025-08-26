from typing import Dict, Any
from ...core.base_agent import BaseAgent
from ...core.registry import register_agent

@register_agent
class AssistantAgent(BaseAgent):
    name = "assistant_agent"

    def handle(self, text: str, context: Dict[str, Any]) -> str:
        system_ref = self.config.get("system_prompt_ref", "assistant")
        prompt = self.prompts.get(system_ref, "You are a precise technical assistant. When in doubt, ask concise questions.")
        model = self.config.get("model")
        llm = self.services["llm"]
        return llm.complete(prompt=prompt, user_text=text, model=model)

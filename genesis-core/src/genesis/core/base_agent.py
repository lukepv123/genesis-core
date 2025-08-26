from typing import Dict, Any

class BaseAgent:
    name: str = "base"
    
    def __init__(self, services: Dict[str, Any], config: Dict[str, Any]):
        self.prompts = services.get("prompts", {})      # Referência aos prompts configurados
        self.services = services
        self.config = config
    
    def on_activate(self) -> None:
        """Called when this agent becomes active."""
        pass
    
    def handle(self, text: str, context: Dict[str, Any]) -> str:
        """Process input and return text response."""
        raise NotImplementedError

from typing import Any, Dict, Optional

class RuntimeState:
    def __init__(self, initial_agent: str = "default_chatbot", config: Optional[Dict[str, Any]] = None):
        self.active_agent = initial_agent
        self.context: Dict[str, Any] = {}
        self._agents: Dict[str, Any] = {}
        self.config: Dict[str, Any] = config or {}

    def switch_agent(self, name: str) -> None:
        self.active_agent = name

    def ensure_agent(self, name: str, agent_cls, services: Dict[str, Any]):
        if name in self._agents:
            return self._agents[name]
        # Preferir config vinda dos services; fallback para a guardada no estado
        cfg = services.get("config") or self.config or {}
        agent = agent_cls(services=services, config=cfg)
        self._agents[name] = agent
        agent.on_activate()
        return agent

from __future__ import annotations
from typing import Any, Dict, TYPE_CHECKING
from .registry import AGENTS, create_command_instances

if TYPE_CHECKING:
    from ..runtime_state import RuntimeState
    from ..bus import EventBus

class Router:
    def __init__(self, services: Dict[str, Any], runtime_state: RuntimeState, bus: EventBus):
        self.services = services
        self.runtime_state = runtime_state
        self.bus = bus
        # ✅ instancia comandos via fábrica (nada de COMMANDS aqui)
        self._commands = create_command_instances(services, runtime_state)

    def route(self, text: str) -> str:
        text = (text or "").strip()
        if not text:
            return ""

        # 1) Tenta comandos
        for cmd in self._commands:
            if cmd.matches(text):
                out = cmd.execute(text)
                if self.bus:
                    self.bus.publish("CommandExecuted", {"command": cmd.__class__.__name__, "text": text})
                return out

        # 2) Cai no agente ativo
        agent_name = self.runtime_state.active_agent
        agent_cls = AGENTS.get(agent_name)
        if not agent_cls:
            return f"Agente '{agent_name}' não encontrado."

        agent = self.runtime_state.ensure_agent(agent_name, agent_cls, self.services)
        result = agent.handle(text, self.runtime_state.context)
        if self.bus:
            self.bus.publish("AgentHandled", {"agent": agent_name, "text": text})
        return result

    # (opcional) API pública para inspeção
    def list_commands(self) -> list[str]:
        return [c.__class__.__name__ for c in self._commands]

    # (opcional) compat temporária com código legado
    @property
    def _command_instances(self):
        return self._commands

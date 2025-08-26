# src/genesis/core/registry.py
from __future__ import annotations
import inspect
from typing import Any, Dict, List, Type, TYPE_CHECKING
from .base_agent import BaseAgent
from .base_command import BaseCommand
if TYPE_CHECKING:
    from ..runtime_state import RuntimeState

COMMAND_CLASSES: List[Type[BaseCommand]] = []
AGENTS: Dict[str, Type[BaseAgent]] = {}

def _validate_command_ctor(cls: Type[BaseCommand]) -> None:
    sig = inspect.signature(cls.__init__)
    params = list(sig.parameters.values())[1:]  # pula self
    msg = (f"{cls.__name__}.__init__ inválido. Esperado: "
           "(self, services: Dict[str, Any], runtime_state: Optional[RuntimeState] = None)")
    if not params or params[0].name != "services":
        raise TypeError(msg + " -> primeiro parâmetro deve ser 'services'.")
    if len(params) >= 2:
        p1 = params[1]
        if p1.name != "runtime_state" or p1.default is inspect._empty:
            raise TypeError(msg + " -> 'runtime_state' deve ser opcional (possuir default).")

def register_command(cls: Type[BaseCommand]) -> Type[BaseCommand]:
    _validate_command_ctor(cls)
    COMMAND_CLASSES.append(cls)
    return cls

def register_agent(cls: Type[BaseAgent]) -> Type[BaseAgent]:
    if not getattr(cls, "name", None):
        raise ValueError(f"Agente sem atributo 'name': {cls}")
    AGENTS[cls.name] = cls
    return cls

def create_command_instances(services: Dict[str, Any], runtime_state: "RuntimeState") -> List[BaseCommand]:
    return [cls(services=services, runtime_state=runtime_state) for cls in COMMAND_CLASSES]

# Compat legado, se alguém ainda importa
COMMANDS = COMMAND_CLASSES


# src/genesis/core/registry.py (trechos relevantes)
COMMAND_CLASSES = []
AGENTS = {}

def register_command(cls):  # valida e registra
    # _validate_command_ctor(cls)  # se estiver usando fail-fast
    COMMAND_CLASSES.append(cls)
    return cls

def create_command_instances(services, runtime_state):
    return [cls(services=services, runtime_state=runtime_state) for cls in COMMAND_CLASSES]

# Alias de compat (se algum outro lugar ainda importar)
COMMANDS = COMMAND_CLASSES

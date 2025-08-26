# src/genesis/core/base_command.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple, TYPE_CHECKING
if TYPE_CHECKING:
    from ..runtime_state import RuntimeState

class BaseCommand(ABC):
    name: str = "command"
    aliases: Tuple[str, ...] = tuple()
    help: str = ""

    def __init__(self, services: Dict[str, Any], runtime_state: Optional["RuntimeState"] = None):
        if services is None:
            raise ValueError("services must not be None")
        self.services = services
        self.runtime_state = runtime_state

    def matches(self, text: str) -> bool:
        lowered = (text or "").strip().lower()
        if self.name and lowered.startswith(self.name):
            return True
        return any(lowered.startswith(a) for a in self.aliases)

    @abstractmethod
    def execute(self, text: str) -> str:
        raise NotImplementedError

# src/genesis/core/action_executor.py
from typing import Callable, Dict

class ActionExecutor:
    def __init__(self):
        self._actions: Dict[str, Callable[..., str]] = {}

    def register(self, name: str, fn: Callable[..., str]) -> None:
        self._actions[name] = fn

    # 👇 novo: idempotente (não sobrescreve se já existir)
    def register_once(self, name: str, fn: Callable[..., str]) -> None:
        self._actions.setdefault(name, fn)

    def has(self, name: str) -> bool:
        return name in self._actions

    def execute(self, name: str, **kwargs) -> str:
        fn = self._actions.get(name)
        if not fn:
            return f"Ação '{name}' não registrada."
        return fn(**kwargs)

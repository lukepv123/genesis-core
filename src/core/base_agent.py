from abc import ABC, abstractmethod
from typing import Dict, List

class BaseAgent(ABC):
    def __init__(self, name: str, system_prompt: str, commands: Dict[str, List[str]]):
        self.name = name
        self.prompt = system_prompt
        self.commands = commands

    @abstractmethod
    def handle_message(self, message: str) -> str:
        pass
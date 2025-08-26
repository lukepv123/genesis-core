from typing import Callable, Dict, List, Any, DefaultDict
from collections import defaultdict

class EventBus:
    def __init__(self):
        self._subs: DefaultDict[str, List[Callable[[Any], None]]] = defaultdict(list)

    def subscribe(self, topic: str, handler: Callable[[Any], None]) -> None:
        self._subs[topic].append(handler)

    def publish(self, topic: str, payload: Any = None) -> None:
        for handler in self._subs.get(topic, []):
            handler(payload)

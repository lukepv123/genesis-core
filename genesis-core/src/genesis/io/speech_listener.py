from typing import Callable, Optional, Dict, Any
from .adapters.google_sr import GoogleSpeechAdapter

class SpeechListener:
    def __init__(self, on_text: Callable[[str], None], config: Dict[str, Any]):
        self.on_text = on_text
        self.config = config
        self.adapter = GoogleSpeechAdapter(cfg=self.config)

    def listen_once(self) -> Optional[str]:
        return self.adapter.listen_once()

    def loop(self, stop_condition: Callable[[], bool]):
        while not stop_condition():
            text = self.listen_once()
            if text:
                self.on_text(text)

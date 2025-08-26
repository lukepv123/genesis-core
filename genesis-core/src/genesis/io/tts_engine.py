from typing import Optional

try:
    import pyttsx3
except Exception:  # pragma: no cover
    pyttsx3 = None

class TTSEngine:
    def __init__(self, voice: Optional[str] = None, rate: Optional[int] = None):
        self.enabled = pyttsx3 is not None
        self.engine = pyttsx3.init() if self.enabled else None
        if self.engine and rate:
            try:
                self.engine.setProperty('rate', rate)
            except Exception:
                pass
        if self.engine and voice:
            try:
                self.engine.setProperty('voice', voice)
            except Exception:
                pass

    def say(self, text: str):
        if not self.enabled or not text:
            return
        self.engine.say(text)
        self.engine.runAndWait()

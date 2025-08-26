from typing import Optional, Dict, Any

try:
    import speech_recognition as sr
except Exception:  # pragma: no cover
    sr = None


class GoogleSpeechAdapter:
    """
    Reads ASR settings from the app config (dict). Expected keys:
      cfg["app"]["locale"]                   -> fallback for language
      cfg["io"]["asr"]["sample_rate"]        -> int (default 16000)
      cfg["io"]["asr"]["language"]           -> str (default app.locale or "en-US")
      cfg["io"]["asr"]["adjust_duration"]    -> float seconds (default 0.3)
      cfg["io"]["asr"]["phrase_time_limit"]  -> int seconds (default 6)
      cfg["io"]["asr"]["energy_threshold"]   -> float (optional)
      cfg["io"]["asr"]["pause_threshold"]    -> float (optional)
    """

    def __init__(self, cfg: Dict[str, Any]):
        self.cfg = cfg or {}
        app_cfg = (self.cfg.get("app") or {})
        asr_cfg = ((self.cfg.get("io") or {}).get("asr") or {})

        self.sample_rate = int(asr_cfg.get("sample_rate", 16000))
        self.language = asr_cfg.get("language") or app_cfg.get("locale") or "en-US"
        self.adjust_duration = float(asr_cfg.get("adjust_duration", 0.3))
        self.phrase_time_limit = int(asr_cfg.get("phrase_time_limit", 6))
        self.energy_threshold = asr_cfg.get("energy_threshold")
        self.pause_threshold = asr_cfg.get("pause_threshold")

        self.enabled = sr is not None
        if self.enabled:
            self.recognizer = sr.Recognizer()
            if self.energy_threshold is not None:
                try:
                    self.recognizer.energy_threshold = float(self.energy_threshold)
                except Exception:
                    pass
            if self.pause_threshold is not None:
                try:
                    self.recognizer.pause_threshold = float(self.pause_threshold)
                except Exception:
                    pass
            self.microphone = sr.Microphone(sample_rate=self.sample_rate)

    def listen_once(self) -> Optional[str]:
        if not self.enabled:
            return None
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=self.adjust_duration)
            audio = self.recognizer.listen(source, phrase_time_limit=self.phrase_time_limit)
        try:
            return self.recognizer.recognize_google(audio, language=self.language)
        except Exception:
            return None

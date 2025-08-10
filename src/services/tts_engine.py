import pyttsx3

class TextToSpeechEngine:
    def __init__(self):
        self.engine = pyttsx3.init()

        # 🔊 Volume máximo
        self.engine.setProperty('volume', 1.0)

        # 🚀 Velocidade de fala mais rápida (Jarvis-style)
        self.engine.setProperty('rate', 140)

        # 🧠 Selecionar voz mais parecida com Jarvis (David ou Zira no Windows)
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "Daniel" in voice.name or "Zira" in voice.name or "Mark" in voice.name:
                self.engine.setProperty('voice', voice.id)
                break

    def configVoz(self, voice_volume: float, voice_speed: int):
        if 0.0 <= voice_volume <= 1.0:
            self.engine.setProperty('volume', voice_volume)
        if 50 <= voice_speed <= 300:
            self.engine.setProperty('rate', voice_speed)

    def falar(self, message: str):
        self.engine.say(message)
        self.engine.runAndWait()

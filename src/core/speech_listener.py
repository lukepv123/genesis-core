import speech_recognition as sr

class SpeechListener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen(self) -> str:
        with self.microphone as source:
            print("🎙️ Waiting for your command...")
            audio = self.recognizer.listen(source)
        try:
            return self.recognizer.recognize_google(audio, language="en")
        except sr.UnknownValueError:
            return "I couldn't understand what was said."
        except sr.RequestError as e:
            return f"Error accessing speech recognition service: {e}"


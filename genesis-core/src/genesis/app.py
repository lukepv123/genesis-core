from typing import Dict, Any
from .io.speech_listener import SpeechListener
from .io.tts_engine import TTSEngine

def run(app: Dict[str, Any]) -> None:
    cfg = app["config"]
    router = app["router"]
    logger = app["logger"]

    wake_word = cfg.get("app", {}).get("wake_word", "protocol").lower()
    tts_cfg = cfg.get("io", {}).get("tts", {})
    tts = TTSEngine(
        voice=tts_cfg.get("voice"),
        rate=tts_cfg.get("rate"),
    )

    active_mode = False

    def on_text(text: str):
        nonlocal active_mode
        logger.info(f"User said: {text}")
        if not active_mode:
            if text.strip().lower().startswith(wake_word):
                active_mode = True
                tts.say("Agent mode activated.")
            return
        response = router.route(text)
        if response:
            tts.say(response)
        if response:
            low = response.lower()
            if "deactivated" in low or "desativado" in low:
                active_mode = False

    # Pass full config so the adapter reads ASR params from config
    listener = SpeechListener(
        on_text=on_text,
        config=cfg,
    )

    try:
        listener.loop(lambda: False)
    except KeyboardInterrupt:
        tts.say("Shutting down. Goodbye.")

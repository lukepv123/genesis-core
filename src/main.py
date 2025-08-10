import os
import yaml
from pathlib import Path
from core.session_manager import SessionManager
from core.agents_router import AgentRouter
from core.offline_command_router import OfflineCommandRouter
from core.action_executor import ActionExecutor
from core.speech_listener import SpeechListener
from services.chatgpt_client import OpenRouterGPTFreeClient
from services.tts_engine import TextToSpeechEngine
from agents.default_chatbot import DefaultChatbot
from agents.assistant_agent import AssistantAgent



if __name__ == "__main__":

    ROOT = Path(__file__).resolve().parent
    with open(ROOT / "config" / "prompts.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)["agents"]


    # 🔐 Lê a chave da variável de ambiente
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise EnvironmentError("❌ API key not found. Please set OPENROUTER_API_KEY before running.")

    # Inicializações
    tts = TextToSpeechEngine()
    speech = SpeechListener()
    executor = ActionExecutor()
    client = OpenRouterGPTFreeClient(api_key=api_key)  # ✅ chave passada explicitamente

    agents = {
        "default_chatbot": DefaultChatbot(client, config['default_chatbot']),
        "assistant_agent": AssistantAgent(client, config['assistant_agent'])
    }

    session = SessionManager()
    router = AgentRouter(session, agents)
    offline_router = OfflineCommandRouter(tts, executor)

    silent_attempts = 0

    tts.falar("Jarvis is running. Say 'protocol' to activate agent mode.")

    while True:
        texto = speech.listen().lower().strip()

        if not texto:
            if offline_router.agent_mode:
                silent_attempts += 1
                print(f"🤫 Silence detected ({silent_attempts}/2)")
                if silent_attempts >= 2:
                    offline_router.deactivate_agent_mode()
                    silent_attempts = 0
                    continue
            continue
        else:
            silent_attempts = 0

        resultado = offline_router.route(texto)

        if resultado == "EXIT":
            if offline_router.agent_mode:
                offline_router.deactivate_agent_mode()
                tts.falar("Exiting agent mode. Say 'protocol' to activate again.")
                print("🔕 Agent mode exited.")
                continue
            else:
                print("👋 Exiting Jarvis.")
                break

        if resultado == "ACTIVATED":
            session.set_active_agent(agents["default_chatbot"])
            continue

        if resultado in ["DEACTIVATED", "BROWSER_OPENED"]:
            continue

        if offline_router.agent_mode:
            if not session.get_active_agent():
                session.set_active_agent(agents["default_chatbot"])

            resposta = router.route(texto)

            if resposta.startswith("CODE: "):
                codigo = resposta.replace("CODE: ", "").strip()
                if not codigo.startswith("MODE_"):
                    resultado = executor.execute_action(codigo)
                    tts.falar(resultado)
                continue

            tts.falar(resposta)
        else:
            print("🤫 Waiting for activation. Say 'protocol' to begin.")

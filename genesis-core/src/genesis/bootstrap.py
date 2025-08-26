# src/genesis/bootstrap.py
from typing import Any, Dict
from .config_loader import load_config
from .logging import setup_logger
from .bus import EventBus
from .runtime_state import RuntimeState
from .core.router import Router
from .core.action_executor import ActionExecutor

# ✅ (se existir no projeto)
try:
    from .services.llm_client import LLMClient
except Exception:
    LLMClient = None  # fallback tratado abaixo

class _SafeLLM:
    """Stub seguro: evita crash se a API não estiver configurada."""
    def __init__(self, inner=None, logger=None):
        self.inner = inner
        self.logger = logger
    def complete(self, prompt: str, user_text: str, model: str | None = None) -> str:
        if self.inner is None:
            return f"[LLM DESABILITADO] {user_text}"
        try:
            # repassa para o cliente real
            return self.inner.complete(prompt=prompt, user_text=user_text, model=model)
        except Exception as e:
            if self.logger: self.logger.warning("LLM error: %s", e)
            return f"[LLM ERROR] {e}"

def create_app(root_dir: str) -> Dict[str, Any]:
    cfg = load_config(root_dir)
    logger = setup_logger("INFO")
    bus = EventBus()
    runtime_state = RuntimeState(initial_agent=cfg.get("app", {}).get("default_agent", "default_chatbot"))

    # --- serviços base ---
    actions = ActionExecutor()

    # 🔹 LLM real (se disponível) ou stub
    llm_service = None
    if LLMClient is not None:
        llm_cfg = cfg.get("services", {}).get("llm", {})
        provider = llm_cfg.get("provider", "openrouter")
        model    = llm_cfg.get("model", "openai/gpt-4o-mini")
        key_env  = llm_cfg.get("api_key_env", "OPENROUTER_API_KEY")
        try:
            llm_service = LLMClient(provider=provider, model=model, api_key_env=key_env)
        except Exception as e:
            logger.warning("Falha ao criar LLMClient: %s", e)

    services: Dict[str, Any] = {
        "logger": logger,
        "config": cfg,
        "prompts": cfg.get("prompts", {}),
        "action_executor": actions,
        # ✅ sempre presente: real ou stub
        "llm": _SafeLLM(inner=llm_service, logger=logger),
    }

    # Autoload de plugins (registra @register_*)
    from . import plugins

    router = Router(services=services, runtime_state=runtime_state, bus=bus)
    return {
        "config": cfg, "logger": logger, "services": services,
        "runtime_state": runtime_state, "bus": bus, "router": router,
    }

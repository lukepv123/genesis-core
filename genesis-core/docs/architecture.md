# Arquitetura – Visão de Alto Nível

1. **Entrada de voz (ASR)** — `io/speech_listener.py` usa `adapters/google_sr.py` para converter áudio → texto.
2. **Roteamento** — `core/router.py` verifica comandos locais primeiro; se não casar, envia ao agente ativo.
3. **Agentes** — Implementam `BaseAgent`; registrados via `registry`. Ex.: `default_chatbot`, `assistant_agent`.
4. **Serviços** — `services/llm_client.py` abstrai o provedor LLM; `services/http.py` centraliza HTTP.
5. **Estado** — `runtime_state.py` guarda agente ativo e contexto da conversa.
6. **Eventos** — `bus.py` permite assinar/publicar eventos internos.
7. **Saída de voz (TTS)** — `io/tts_engine.py` fala a resposta.
8. **Orquestração** — `bootstrap.py` monta dependências; `app.py` gerencia o loop principal.

Fluxo:
Voz → ASR → Router → (Command | Agent) → Resposta → TTS
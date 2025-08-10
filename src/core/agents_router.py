class AgentRouter:
    def __init__(self, session_manager, agents: dict):
        self.session = session_manager
        self.agents = agents

    def route(self, message: str) -> str:
        agent = self.session.get_active_agent()
        response = agent.handle_message(message)

        # Detecta comando de troca de modo
        if response.startswith("CODE: SWITCH_TO_ASSISTANT"):
            self.session.set_active_agent(self.agents["assistant_agent"])
            return "Switched to assistant mode."

        elif response.startswith("CODE: SWITCH_TO_DEFAULT"):
            self.session.set_active_agent(self.agents["default_chatbot"])
            return "Switched to default mode."

        return response

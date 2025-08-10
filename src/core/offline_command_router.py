class OfflineCommandRouter:
    def __init__(self, tts, executor):
        self.tts = tts
        self.executor = executor
        self.commands = {
            "protocol": self.activate_agent_mode,
            "deactivate": self.deactivate_agent_mode,
            "cancel protocol": self.deactivate_agent_mode,
            "exit": self.exit_program,
            "open browser": self.open_browser
        }
        self.agent_mode = False
        self.exit_flag = False

    def route(self, text: str) -> str:
        # Busca exata
        for trigger, action in self.commands.items():
            if trigger in text:
                return action()

        # Caso esteja no modo ativo mas sem comando reconhecido
        if not self.agent_mode:
            print("🤫 Waiting for 'protocol' to activate agent mode.")
        return ""

    def activate_agent_mode(self):
        self.agent_mode = True
        self.tts.falar("Protocol activated.")
        print("✅ Agent mode is now ON.")
        return "ACTIVATED"

    def deactivate_agent_mode(self):
        self.agent_mode = False
        self.tts.falar("Protocol deactivated.")
        print("🚫 Agent mode is now OFF.")
        return "DEACTIVATED"

    def exit_program(self):
        self.exit_flag = True
        self.tts.falar("Shutting down.")
        print("👋 Exiting Jarvis.")
        return "EXIT"

    def open_browser(self):
        result = self.executor.execute_action("OPEN_BROWSER")
        self.tts.falar(result)
        return "BROWSER_OPENED"

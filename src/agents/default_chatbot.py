from core.base_agent import BaseAgent

class DefaultChatbot(BaseAgent):
    def __init__(self, client, config):
        super().__init__("default_chatbot", config['system_prompt'], config['commands'])
        self.client = client

    def handle_message(self, message: str) -> str:
        for code, triggers in self.commands.items():
            if any(trigger in message.lower() for trigger in triggers):
                return f"CODE: {code}"
        return self.client.get_chat_response([
            {"role": "system", "content": self.prompt},
            {"role": "user", "content": message}
        ])
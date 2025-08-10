class SessionManager:
    def __init__(self):
        self.active_agent = None

    def set_active_agent(self, agent):
        self.active_agent = agent

    def get_active_agent(self):
        return self.active_agent
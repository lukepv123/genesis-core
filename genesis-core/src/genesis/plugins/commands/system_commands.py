from ...core.base_command import BaseCommand
from ...core.registry import register_command

@register_command
class HelpCommand(BaseCommand):
    name = "ajuda"
    aliases = ("help", "comandos")
    help = "Lista comandos básicos do sistema."

    def execute(self, text: str) -> str:
        return (
            "Comandos:\n"
            "- 'agente <nome>' para trocar de agente (ex.: agente default_chatbot)\n"
            "- 'desativar' para encerrar o modo agente\n"
            "- 'ajuda' para esta ajuda"
        )

@register_command
class DeactivateCommand(BaseCommand):
    name = "desativar"
    aliases = ("deactivate",)
    help = "Sai do modo agente."

    def execute(self, text: str) -> str:
        return "Agent mode deactivated."

@register_command
class AgentCommand(BaseCommand):
    name = "agente"
    aliases = ("agent",)
    help = "Troca o agente ativo. Ex.: 'agente assistant_agent'"

    def execute(self, text: str) -> str:
        parts = (text or "").split()
        if len(parts) < 2:
            return "Informe o nome do agente. Ex.: 'agente default_chatbot'"
        agent_name = parts[1].strip()
        if not self.runtime_state:
            return "Estado indisponível."
        self.runtime_state.switch_agent(agent_name)
        return f"Agente ativo: {agent_name}"

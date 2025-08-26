# src/genesis/plugins/commands/media_commands.py
from ...core.base_command import BaseCommand
from ...core.registry import register_command



# @register_command
# class TimeNowCommand(BaseCommand):
#     name = "hora"
#     aliases = ("que horas são", "time")
#     help = "Informa a hora atual."

#     def execute(self, text: str) -> str:
#         execu = self.services.get("action_executor")
#         if not execu:
#             return "Executor de ações indisponível."
#         return execu.time_now() if hasattr(execu, "time_now") else execu.execute("time_now")

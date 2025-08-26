# src/genesis/plugins/commands/open_browser.py
from urllib.parse import quote_plus
from ...core.base_command import BaseCommand
from ...core.registry import register_command

@register_command
class OpenBrownser(BaseCommand):
    # manterei o nome como você escreveu; o matcher usa startswith em lower()
    name = "openbrownser"
    aliases = (
        "open brownser", "open browser", "brownser", "browser",
        "fat ass", "no"
    )
    help = "Abre o Google. Ex.: 'open browser' ou 'open browser gatinhos'"

    def execute(self, text: str) -> str:
        parts = (text or "").strip().split(maxsplit=1)
        if len(parts) == 1 or not parts[1].strip():
            url = "https://www.google.com/?hl=pt-BR&gl=BR"
        else:
            query = parts[1].strip()
            url = f"https://www.google.com/search?hl=pt-BR&gl=BR&q={quote_plus(query)}"

        execu = self.services.get("action_executor")
        if not execu:
            return "Executor de ações indisponível. Configure 'action_executor' no bootstrap."

        # 🔹 DI de verdade: o comando fornece a implementação e registra uma vez
        execu.register_once("open_url", self._open_url)
        return execu.execute("open_url", url=url)

    # ----- implementação da ação (lógica do comando) -----
    def _open_url(self, url: str) -> str:
        import webbrowser
        try:
            webbrowser.open(url, new=2)
            return f"Abrindo: {url}"
        except Exception as e:
            return f"Falha ao abrir URL: {e}"

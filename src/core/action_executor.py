import subprocess
import platform
import datetime
import webbrowser

class ActionExecutor:
    def execute_action(self, command_code: str) -> str:
        match command_code:
            case "OPEN_IDE":
                return self._open_ide()
            case "CURRENT_TIME":
                return self._get_current_time()
            case "OPEN_BROWSER":
                return self._open_browser()
            case "OPEN_CHROME":
                return self._open_specific_browser("chrome")
            case "OPEN_OPERA":
                return self._open_specific_browser("opera")
            case "OPEN_FIREFOX":
                return self._open_specific_browser("firefox")
            case "CREATE_REMINDER" | "OPEN_CALENDAR":
                return "Function not yet implemented."
            case _:
                return "Unknown command."

    def _open_ide(self):
        try:
            subprocess.Popen(["code"])
            return "Opening Visual Studio Code."
        except Exception as e:
            return f"Could not open the IDE: {e}"

    def _get_current_time(self):
        now = datetime.datetime.now()
        return f"It's {now.hour} hours and {now.minute} minutes."

    def _open_browser(self):
        try:
            webbrowser.open("http://www.google.com")
            return "Opening default web browser."
        except Exception as e:
            return f"Failed to open browser: {e}"

    def _open_specific_browser(self, browser_name: str):
        try:
            os_name = platform.system()

            if os_name == "Windows":
                subprocess.Popen([browser_name], shell=True)
            elif os_name == "Linux":
                subprocess.Popen([browser_name])
            elif os_name == "Darwin":  # macOS
                subprocess.Popen(["open", "-a", browser_name])
            else:
                return "Unsupported OS for browser launching."

            return f"Opening {browser_name}."
        except Exception as e:
            return f"Could not open {browser_name}: {e}"

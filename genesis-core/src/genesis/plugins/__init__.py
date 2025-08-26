from __future__ import annotations
import pkgutil
import importlib

def _autoload_subpkg(subpkg: str) -> None:
    full = f"{__name__}.{subpkg}"
    try:
        pkg = importlib.import_module(full)  # garante entrada em sys.modules
    except ModuleNotFoundError:
        return
    for m in pkgutil.iter_modules(pkg.__path__, full + "."):
        importlib.import_module(m.name)  # executa os @register_*

_autoload_subpkg("agents")
_autoload_subpkg("commands")

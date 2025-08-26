import os
import yaml
from typing import Dict, Any

def load_yaml(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
        return data

def load_config(root_dir: str) -> Dict[str, Any]:
    app_cfg = load_yaml(os.path.join(root_dir, "config", "app.yaml"))
    prompts = load_yaml(os.path.join(root_dir, "config", "prompts.yaml"))
    if "prompts" in prompts:
        app_cfg["prompts"] = prompts["prompts"]
    return app_cfg

import json
from pathlib import Path



class ComplianceRules:
    def __init__(self, config_path: str = None):
        if config_path is None:
            # Always resolve relative to project root
            config_path = Path(__file__).resolve().parents[1] / "config/compliance.json"
        self.rules = self._load_rules(config_path)


    def _load_rules(self, config_path: str):
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Compliance config not found: {config_path}")
        with open(config_file, "r") as f:
            return json.load(f)

    def get_rules(self):
        return self.rules

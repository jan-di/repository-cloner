from dataclasses import dataclass


@dataclass
class GlobalContext:
    working_dir: str
    config_path: str

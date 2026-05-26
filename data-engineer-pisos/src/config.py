from pathlib import Path

from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    idealista_api_key: str = ""
    idealista_api_secret: str = ""
    duckdb_path: str = "data/pisos.duckdb"
    log_level: str = "INFO"

    model_config = {"env_file": PROJECT_ROOT / ".env", "env_file_encoding": "utf-8"}


settings = Settings()

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret: str


settings = Settings()  # type: ignore

BASE_DIR = Path(__file__).parent
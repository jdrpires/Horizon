from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="HORIZON_", frozen=True)

    env: str = "local"
    log_level: str = "INFO"


def get_settings() -> Settings:
    return Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Public
    debug_apply_any_bearer_tokens: bool = False
    dev_routes_enabled: bool = False
    app_name: str = "My API"
    database_url: str
    redis_url: str = "redis://localhost:6379"

    # Private
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_ttl_minutes: int = 30

# читает .env + переменные окружения
settings = Settings()
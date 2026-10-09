from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Read once from environment variables, then from backend/.env.

    No defaults for secrets: a missing DATABASE_URL or JWT_SECRET fails at startup.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    # Signs access tokens with HMAC-SHA256, which needs at least 32 bytes of key.
    jwt_secret: str = Field(min_length=32)
    jwt_expire_minutes: int = 60 * 24 * 7
    cors_origins: list[str] = ["http://localhost:8081"]


settings = Settings()

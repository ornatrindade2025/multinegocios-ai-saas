from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    OPENAI_API_KEY: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()

if not settings.SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is not set.")

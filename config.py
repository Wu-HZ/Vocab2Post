from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    WP_URL: str
    WP_USER: str
    WP_APP_PASSWORD: str
    AI_API_KEY: str
    PORT: int = 8940

    class Config:
        env_file = ".env"

settings = Settings()

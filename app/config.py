from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "MatchMeter"
    debug: bool = False
    database_url: str = "sqlite:///./app.db"
    openai_api_key: str

    class Config:
        env_file = ".env"

settings = Settings()
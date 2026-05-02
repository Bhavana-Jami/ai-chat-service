from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    allowed_origins: list[str] = ["http://localhost:5173/"]
    port: int = 8000                

    class Config:
        env_file = ".env"
        extra = "ignore"           

settings = Settings()
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "mysecretkey"  # valor padrão (usado se não houver no .env)

    class Config:
        env_file = ".env"  # agora sim o Pydantic carrega .env corretamente

settings = Settings()

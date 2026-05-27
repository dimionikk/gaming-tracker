from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    redis_url: str

    class Config:
        env_file = ".env"


settings = Settings()
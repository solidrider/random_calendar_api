from pydantic import BaseSettings


class Settings(BaseSettings):
    CLIENT_ID: str

    class Config:
        env_file = "../.env"

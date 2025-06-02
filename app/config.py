from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    Database_Host: str
    Database_Username: str
    Database_Password: str
    Database_Name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    Database_Port: str

    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str

    class Config:
        env_file = ".env"


# Instantiate the settings object
settings = Settings()

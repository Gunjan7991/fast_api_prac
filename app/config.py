from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    IP_Address: str
    Database_Username: str
    Database_Password: str
    Database_Name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    Database_Port: str

    class Config:
        env_file = ".env"


settings = Settings()

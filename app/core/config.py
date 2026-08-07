from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    DEBUG: bool
    API_V1_STR: str 
    SECRET_KEY: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    DATABASE_URL: str
    DATABASE_URL_ALEMBIC: str
    model_config = SettingsConfigDict( env_file=".env", case_sensitive=True)

settings = Settings()

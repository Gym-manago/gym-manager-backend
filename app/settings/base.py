from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    db_name: str
    postgres_username: str
    postgres_pass: str
    postgres_host: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
DB_NAME = settings.db_name
POSTGRES_USERNAME = settings.postgres_username
POSTGRES_PASS = settings.postgres_pass
POSTGRES_HOST = settings.postgres_host

DATABASE_URL = (
    f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASS}@{POSTGRES_HOST}/{DB_NAME}"
)

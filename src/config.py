from datetime import timedelta
from pathlib import Path
from os import path

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


env_path = Path(__file__).parent.parent / '.env'


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASS: str
    REDIS_DATA_PATH: Path

    MAIL_HOST: str
    MAIL_PORT: int
    MAIL_USER: EmailStr
    MAIL_PASS: str
    READ_MAILBOX: str
    MAIL_PROJECT_ID: int
    BOT_USER_ID: int

    JWT_SECRET: str
    ACCESS_TOKEN_TTL: int

    APP_DEBUG: bool
    APP_HOST: str
    APP_PORT: int

    MEDIA_PATH: Path
    ALLOWED_TEXT_FILE_EXTENSIONS: set
    ALLOWED_IMAGE_FILE_EXTENSIONS: set

    src_path: Path = Path(__file__).parent

    @property
    def database_url_psycopg(self):
        return "postgresql+psycopg://{user}:{password}@{host}:{port}/{name}".format(
            user=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST,
            port=self.DB_PORT,
            name=self.DB_NAME,
        )

    @property
    def access_token_ttl_timedelta(self):
        return timedelta(seconds=self.ACCESS_TOKEN_TTL)

    @property
    def redis_url(self):
        return 'redis://{user}:{password}@{host}:{port}/0'.format(
            user='',
            password=self.REDIS_PASS,
            host=self.REDIS_HOST,
            port=self.REDIS_PORT
        )

    @property
    def refresh_token_ttl_timedelta(self):
        return timedelta(seconds=self.REFRESH_TOKEN_TTL)

    @property
    def allowed_file_extensions(self):
        return (self.ALLOWED_TEXT_FILE_EXTENSIONS |
                self.ALLOWED_IMAGE_FILE_EXTENSIONS)

    if path.exists(env_path):
        model_config = SettingsConfigDict(env_file=env_path)


settings = Settings()

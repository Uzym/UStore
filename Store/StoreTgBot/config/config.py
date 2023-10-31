from dataclasses import dataclass

from dotenv import load_dotenv

from .base import getenv, ImproperlyConfigured


@dataclass
class TelegramBotConfig:
    token: str


@dataclass
class Config:
    tg_bot: TelegramBotConfig
    api_key: str
    s3_api_key: str


def load_config() -> Config:
    load_dotenv()

    return Config(tg_bot=TelegramBotConfig(token=getenv("TOKEN")), api_key=getenv("API_URL"),
                  s3_api_key=getenv("S3_API_URL"))

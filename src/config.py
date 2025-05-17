import sys
from enum import StrEnum
from pathlib import Path
from typing import Literal

from loguru import logger
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ("settings",)


class _ALG(StrEnum):
    HS256 = "HS256"
    HS384 = "HS384"
    HS512 = "HS512"


class JWTSettings(BaseModel):
    secret_key: SecretStr = SecretStr("jfeiwo8392h0)_9fu0UJF()EW323j$_")
    access_token_expire_minutes: int = 24 * 60 * 60
    access_token_algorithm: _ALG = _ALG.HS256


class SentrySettings(BaseModel):
    api_dsn: SecretStr = SecretStr("")
    service_dsn: SecretStr = SecretStr("")
    enable_tracing: bool = True
    traces_sample_rate: float = 1.0
    profiles_sample_rate: float = 1.0


class Config(BaseSettings):
    root_dir: Path = Path(__file__).parent.parent.resolve()
    logging_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    project_title: str = "Tokemons API"
    project_description: str = "Open API to interact with Tokemons data"

    jwt: JWTSettings = JWTSettings()

    sentry: SentrySettings = SentrySettings()
    allowed_hosts: list[str] = []
    tonapi_url: str = "https://tonapi.io/"

    model_config = SettingsConfigDict(
        env_file=f"{root_dir}/.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        validate_assignment=True,
        env_nested_delimiter="__",
        extra="ignore",  # ignores extra keys from env file
    )


settings = Config()

# Logging Configuration
logger.remove(0)

_logtime = "<green>{time:YYYY-MM-DD HH:mm:ss}</green>"
_loglevel = "<red>[{level}]</red>"
_logpath = "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>"
_logmsg = "<green>{message}</green>"
logger.add(
    sys.stderr,
    format=f"{_logtime} | {_loglevel} | {_logpath}: {_logmsg}",
    colorize=True,
    level=settings.logging_level,
    backtrace=True,
    diagnose=True,
)

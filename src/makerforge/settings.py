from pydantic import AliasChoices, Field, RedisDsn
from pydantic_settings import BaseSettings, CliSubCommand, SettingsConfigDict

from .exchanges.coinmate.sub.settings import CoinmateSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", cli_parse_args=True, env_nested_delimiter="__"
    )
    redis_dsn: RedisDsn = Field(
        RedisDsn("redis://localhost:6379/1"),
        validation_alias=AliasChoices("service_redis_dsn", "redis_url", "redis-url"),
    )
    coinmate: CliSubCommand[CoinmateSettings]

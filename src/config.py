from dataclasses import dataclass
import logging
import sys
from dataclasses import dataclass
from typing import List, Union, Optional

from environs import Env, EnvError
from sqlalchemy.engine.url import URL


@dataclass
class DbConfig:
    """
        Database configuration class.
        This class holds the settings for the database, such as host, password, port, etc.

        Attributes
        ----------
        host : str
            The host where the database server is located.
        password : str
            The password used to authenticate with the database.
        user : str
            The username used to authenticate with the database.
        database : str
            The name of the database.
        port : int
            The port where the database server is listening.
        """

    password: str
    host: str
    user: str
    database: str
    port: int

    @staticmethod
    def construct_sqlalchemy_url(env, driver="asyncpg") -> str:
        """
        Constructs and returns a SQLAlchemy URL for this database configuration.
        """

        uri = URL.create(
            drivername=f"postgresql+{driver}",
            username=env.str('DB_USER', "postgres"),
            password=env.str('DB_PASS'),
            host="postgres" if sys.platform != 'win32' else '127.0.0.1',
            port=env.int('DB_PORT', 5432),
            database=env.str('DB_NAME', "vpn_bot"),
        )
        return uri.render_as_string(hide_password=False)


@dataclass
class RedisConfig:
    """
    Redis configuration class.

    Attributes
    ----------
    redis_pass : Optional(str)
        The password used to authenticate with Redis.
    redis_port : Optional(int)
        The port where Redis server is listening.
    redis_host : Optional(str)
        The host where Redis server is located.
    """

    redis_pass: Optional[str]
    redis_port: int
    redis_host: str = "redis_custom_vpn_bot"

    def dsn(self) -> str:
        """
        Constructs and returns a Redis DSN (Data Source Name) for this database configuration.
        """
        if self.redis_pass:
            return f"redis://:{self.redis_pass}@{self.redis_host}:{self.redis_port}/0"
        else:
            return f"redis://{self.redis_host}:{self.redis_port}/0"

    @staticmethod
    def from_env(env: Env):
        """
        Creates the RedisConfig object from environment variables.
        """
        redis_pass = env.str("REDIS_PASSWORD", None)
        redis_port = env.int("REDIS_PORT", 6379)
        redis_host = env.str("REDIS_HOST", "redis")

        return RedisConfig(
            redis_pass=redis_pass, redis_port=redis_port, redis_host=redis_host
        )

@dataclass
class TgBot:
    token: str

    @staticmethod
    def from_env(env: Env):
        token = env.str('BOT_TOKEN')
        return TgBot(token)
@dataclass
class Config:
    db_url: str
    redis: RedisConfig
    tg_bot: TgBot

def load_config():
    env = Env()
    env.read_env('.env')
    return Config(
        db_url=DbConfig.construct_sqlalchemy_url(env),
        tg_bot=TgBot.from_env(env),
        redis=RedisConfig.from_env(env)
    )
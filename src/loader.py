from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import redis.asyncio as redis
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage

from config import load_config

config = load_config()

bot = Bot(token=config.tg_bot.token,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview_is_disabled=True))

redis_cli = redis.Redis(host='redis', password=config.redis.redis_pass, decode_responses=True)

dp = Dispatcher(storage=RedisStorage.from_url(
            config.redis.dsn(),
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        ))
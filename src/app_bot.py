import asyncio
import logging
import betterlogging as bl
from aiogram import Bot
from aiogram.types import BotCommandScopeDefault, BotCommand

from bot import register_global_middlewares
from loader import bot, dp, config
from tgbot.handlers import routers_list
from tgbot.services import broadcaster


def setup_logging():
    """
    Set up logging configuration for the application.

    This method initializes the logging configuration for the application.
    It sets the log level to INFO and configures a basic colorized log for
    output. The log format includes the filename, line number, log level,
    timestamp, logger name, and log message.

    Returns:
        None

    Example usage:
        setup_logging()
    """
    log_level = logging.DEBUG
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=log_level,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    # logger_init = logging.getLogger(__name__)
    # api_handler = APINotificationHandler(config.tg_bot.token, config.tg_bot.admin_ids[0])
    # api_handler.setLevel(logging.ERROR)
    # logger_init.addHandler(api_handler)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

async def register_commands():
    commands_en = [
        BotCommand(command='start', description='Main Menu 🏠')
                   ]
    await bot.set_my_commands(commands_en, BotCommandScopeDefault(), language_code='en')
    commands_ru = [
        BotCommand(command='start', description='Главное меню 🏠'),
                   ]
    await bot.set_my_commands(commands_ru, BotCommandScopeDefault(), language_code='ru')

async def on_startup(bot: Bot):

    await register_commands()
    await broadcaster.broadcast(bot, config.tg_bot.admin_ids, "Бот запущен")

async def main_polling():
    dp.include_routers(*routers_list)

    register_global_middlewares(dp, config)
    await on_startup(bot)
    await bot.delete_webhook()
    await dp.start_polling(bot)
    logging.info("Starting bot")


if __name__ == '__main__':
    setup_logging()
    try:
        asyncio.run(main_polling())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот выключен!")

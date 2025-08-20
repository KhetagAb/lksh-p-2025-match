import asyncio
import logging
import sys
import traceback
from types import TracebackType

from lkshmatch.tg_bot.bot import bot

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

bot_logger = logging.getLogger('telegram_bot')
bot_logger.setLevel(logging.DEBUG)


def log_exception(exc_type: type[BaseException], exc_value: BaseException, exc_traceback: TracebackType | None) -> None:
    if issubclass(exc_type, KeyboardInterrupt):
        return

    bot_logger.error(
        "Unhandled exception:",
        exc_info=(exc_type, exc_value, exc_traceback)
    )


sys.excepthook = log_exception


async def run_bot_with_error_handling() -> None:
    try:
        bot_logger.info("Starting Telegram bot...")
        await bot.polling(non_stop=True)
    except Exception as e:
        bot_logger.error(f"Critical bot error: {e}")
        bot_logger.error(f"Full stack trace:\n{traceback.format_exc()}")
        raise


if __name__ == "__main__":
    asyncio.run(run_bot_with_error_handling())

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from handlers import on_start, on_new, on_tutor, on_message
import env
import asyncio


async def main():
  try:
    bot = Bot(token=env.BOT_TOKEN, parse_mode=ParseMode.MARKDOWN)
    dp = Dispatcher()

    handlers = [
        ([CommandStart()], on_start),
        ([Command("new")], on_new),
        ([Command("tutor")], on_tutor),
        ([], on_message),
    ]

    for filters, handler in handlers:
      dp.message(*filters)(handler)

    await dp.start_polling(bot)

  finally:
    await bot.close()


asyncio.run(main())

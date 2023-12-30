from os import getenv
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
import handlers

BOT_TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()


async def main():
  bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.MARKDOWN)
  await dp.start_polling(bot)


@dp.message(CommandStart())
async def on_start(message: types.Message): await handlers.on_start(message)


@dp.message(Command("new"))
async def on_new(message: types.Message): await handlers.on_new(message)


@dp.message(Command("tutor"))
async def on_tutor(message: types.Message): await handlers.on_tutor(message)


@dp.message()
async def on_message(message: types.Message): await handlers.on_message(message)

asyncio.run(main())

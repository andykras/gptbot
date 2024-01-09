from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
import asyncio

# Start by organizing your project into the following directory structure:
# project/
# ├── gptbot1/
# │   └── git clone https://github.com/andykras/gptbot.git .
# │
# ├── gptbot2/
# │   └── git clone https://github.com/andykras/gptbot.git .
# │
# └── multibot.py # put this file above bot folders.
#
# This file will contain the code for managing your bots:
# python multibot.py

import gptbot1
import gptbot2

tokens = [
    gptbot1.env.BOT_TOKEN,
    gptbot2.env.BOT_TOKEN,
]

routers = [
    gptbot1.handlers.router,
    gptbot2.handlers.router,
]


async def main():
  tasks = []
  for token, router in zip(tokens, routers):
    bot = Bot(token=token, parse_mode=ParseMode.MARKDOWN)
    dp = Dispatcher()
    dp.include_router(router)
    tasks.append(dp.start_polling(bot, handle_signals=False, polling_timeout=100))

  await asyncio.gather(*tasks)


try:
  asyncio.run(main())
except KeyboardInterrupt:
  print('stopped')
  pass

from aiogram import types
from actions import change_assistant, handle_response
from client import get_thread, get_assistant
from logger import create_logger
from translate import _t

logger = create_logger("handlers")


async def on_start(message: types.Message) -> None:
  await message.answer(text=_t("bot.welcome", name=message.from_user.full_name, id=message.from_user.id))
  logger.info(f"on_start:{message.from_user.username}:{message.from_user.id}")


async def on_new(message: types.Message) -> None:
  await message.answer(_t("bot.new_chat"))
  thread = await get_thread(message.from_user.id, new_thread=True)
  logger.debug(thread)


async def on_tutor(message: types.Message) -> None:
  tutors = await get_assistant()
  logger.info(tutors)
  await message.answer(
      _t("bot.new_tutor", tutors="\n".join([f"`{id}`: {info['desc']}" for id, info in tutors.items()])),
      reply_markup=types.ReplyKeyboardMarkup(
          keyboard=[[types.KeyboardButton(text=id) for id, _ in tutors.items()]],
          resize_keyboard=True
      )
  )


async def on_message(message: types.Message) -> None:
  try:
    if message.text in await get_assistant():
      await change_assistant(message)
    else:
      await handle_response(message)
  except TypeError as error:
    logger.error(error)
    await message.answer(_t("bot.error_in_the_code"))

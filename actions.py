import time
import asyncio
from typing import List
from openai.types import beta
from aiogram import types

from .client import client, get_thread, get_assistant
from .logger import create_logger
from .translate import _t
from . import env
from .helpers import ChatActions, is_valid_markdown, escape_markdown
from .users import is_group_bot
from .message_queues import QueueController, thread_lock


logger = create_logger(__name__)


async def change_assistant(message: types.Message):
  tutor = message.text
  user_id = message.from_user.id
  await message.answer(_t("bot.your_tutor", tutor=tutor), reply_markup=types.ReplyKeyboardRemove())
  assistant = await get_assistant(user_id, tutor)
  logger.info(f"new_assistant:{user_id}:{tutor}:{assistant.id}")


async def handle_response(message: types.Message):
  user_id = message.from_user.id
  username = message.from_user.username

  logger.info(f"user:{username}:{user_id}\n\t{message.md_text}")

  thread = await get_thread(user_id)
  logger.debug(f"handle_response:{thread}")

  if not QueueController.start_queue(thread, message):
    return

  assistant = await get_assistant(user_id)
  logger.debug(f"handle_response:{assistant}")

  delay = env.GROUP_BOT_RESPONSE_DELAY if is_group_bot() else env.BOT_RESPONSE_DELAY
  if delay > 0:
    await QueueController.wait_next(delay, thread, user_id)

  async with thread_lock(thread.id, user_id) as messages:
    await add_messages_to_thread(thread, messages)
    await process_message(thread, assistant, message)


async def process_message(thread: beta.Thread, assistant: beta.Assistant, message: types.Message):
  logger.debug(f"process_message:{thread.id}:{message.message_id}")

  run = await client.beta.threads.runs.create(
      thread.id,
      assistant_id=assistant.id,
      instructions=_t("gpt.instructions",
                      name=message.from_user.first_name,
                      id=message.from_user.id,
                      full_name=message.from_user.full_name,
                      instructions=assistant.instructions)
  )

  start_time = time.time()
  while True:
    logger.info(f"process_message:status:{run.status}")

    if run.status == "completed":
      await retrieve_messages(thread.id, run.id, message)
      logger.info("process_message:done")
      break
    elif run.status in ["failed", "cancelled", "expired"]:
      logger.info("process_message:failed")
      break
    else:
      await ChatActions.send_typing(message)
      await asyncio.sleep(env.RUN_STATUS_POLL_INTERVAL)

    run = await client.beta.threads.runs.retrieve(
        run.id,
        thread_id=thread.id
    )
  end_time = time.time()
  logger.debug(f"process_message:reponse time: {end_time - start_time:.2f}s")


async def retrieve_messages(thread_id, run_id, message: types.Message):
  run_steps = await client.beta.threads.runs.steps.list(
      thread_id=thread_id,
      run_id=run_id
  )

  for step in run_steps.data:
    if step.type == "message_creation":
      message_id = step.step_details.message_creation.message_id

      msg = await client.beta.threads.messages.retrieve(
          message_id=message_id,
          thread_id=thread_id
      )

      content = msg.content[0].text.value
      if content:
        escaped = not is_valid_markdown(content)
        if escaped:
          content = escape_markdown(content)
        logger.info(f"retrieve_messages:{msg.role}:{step.assistant_id}:escaped={escaped}:\n\t{content}")
        await message.answer(content)


async def add_messages_to_thread(thread: beta.Thread, messages: List[types.Message]):
  user_request = await client.beta.threads.messages.create(
      thread.id,
      role="user",
      content="\n".join(message.md_text for message in messages)
  )
  logger.debug(f"add_message_to_thread:{user_request.id}")

import asyncio
import time
from typing import Dict, List
from collections import defaultdict
from openai.types import beta
from aiogram import types
from contextlib import asynccontextmanager


class Messages:
  def __init__(self):
    self.queue: Dict[int, List[types.Message]] = defaultdict(list)  # user_id -> messages
    self.has_active_run = asyncio.Event()
    self.has_active_run.set()


class QueueController:
  data: Dict[str, Messages] = {}  # thread_id -> user's message queue

  @staticmethod
  def start_queue(thread: beta.Thread, message: types.Message):
    messages = QueueController.data.setdefault(thread.id, Messages())
    user_id = message.from_user.id
    messages.queue[user_id].append(message)
    return len(messages.queue[user_id]) == 1

  @staticmethod
  async def wait_next(delay: float, thread: beta.Thread, user_id: int):
    messages = QueueController.data[thread.id].queue[user_id]
    message_time = messages[-1].date.timestamp()

    while time.time() - message_time < delay:
      time_to_wait = message_time + delay - time.time()

      await asyncio.sleep(time_to_wait)
      message_time = messages[-1].date.timestamp()


@asynccontextmanager
async def thread_lock(thread_id, user_id):
  messages = QueueController.data.get(thread_id)

  await messages.has_active_run.wait()
  messages.has_active_run.clear()

  try:
    yield messages.queue.pop(user_id)

  finally:
    messages.has_active_run.set()
    if not messages.queue:
      QueueController.data.pop(thread_id, None)

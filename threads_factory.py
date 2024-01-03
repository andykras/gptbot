import yaml
from datetime import datetime, timedelta
from openai import AsyncOpenAI
from logger import create_logger

logger = create_logger(__name__)


def threads_factory(client: AsyncOpenAI):
  storage = "threads.yaml"
  threads = {}
  cache = {}

  def load():
    try:
      with open(storage, 'r') as file:
        return yaml.safe_load(file) or {}
    except FileNotFoundError:
      return {}

  def save():
    with open(storage, 'w') as file:
      yaml.dump(threads, file, allow_unicode=True)

  async def get_thread(user_id, new_thread=False):
    now = datetime.now()

    if not threads:
      threads.update(load())

    if new_thread:
      threads.pop(user_id, None)

    needs_update = (
        user_id not in threads or
        user_id not in cache or
        now - cache[user_id]["expire_date"] > timedelta(days=1)
    )

    if needs_update:
      if user_id not in threads:
        thread = await client.beta.threads.create()
        threads[user_id] = thread.id
        logger.info(f"new thread: {user_id}, {thread.id}")
      else:
        thread = await client.beta.threads.retrieve(threads[user_id])
        logger.info(f"retrieve thread: {user_id}, {thread.id}")

      cache[user_id] = {
          "expire_date": now + timedelta(days=1),
          "thread": thread
      }
      save()

    return cache[user_id]["thread"]

  return get_thread

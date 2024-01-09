import yaml
from datetime import datetime, timedelta
from aiogram import types
from openai import AsyncOpenAI
from .logger import create_logger
from pathlib import Path

logger = create_logger(__name__)


def assistants_factory(client: AsyncOpenAI):
  storage = Path(__file__).parent / "tutors.yaml"
  tutors = {}
  user_prefs = {}
  cache = {}

  def load():
    defaults = [
        # tutors
        {
            "default": {"desc": "default assistant", "id": "asst_id_from_openai"},
        },
        # user_prefs
        {}
    ]
    try:
      with open(storage, 'r') as file:
        return yaml.safe_load(file) or defaults
    except FileNotFoundError:
      logger.warn(f"{storage} not found")
      return defaults

  def save():
    with open(storage, 'w') as file:
      yaml.dump([tutors, user_prefs], file, allow_unicode=True)

  async def get_assistant(user_id=None, new_tutor=None):
    now = datetime.now()

    if not tutors:
      data = load()
      tutors.update(data[0] if len(data) > 0 else {})
      user_prefs.update(data[1] if len(data) > 1 else {})

    if user_id is None:
      return tutors

    if new_tutor in tutors:
      assistant_id = tutors[new_tutor]["id"]
      user_prefs[user_id] = new_tutor
      cache.pop(user_id, None)
      save()
    else:
      default_assistant = tutors.get("default", next(iter(tutors.values())))
      assistant_id = tutors.get(user_prefs.get(user_id), default_assistant)["id"]

    if user_id not in cache or now - cache[user_id]["expire_date"] > timedelta(days=1):

      assistant = await client.beta.assistants.retrieve(assistant_id)
      logger.info(f"retrieve assistant: {user_id}, {assistant.id}")

      cache[user_id] = {
          "expire_date": now + timedelta(days=1),
          "assistant": assistant
      }

    return cache[user_id]["assistant"]

  def asst_filter(message: types.Message):
    return message.text in tutors

  return (get_assistant, asst_filter)

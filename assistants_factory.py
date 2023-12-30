import yaml
from datetime import datetime, timedelta
from openai import AsyncOpenAI
from logger import createLogger

logger = createLogger("users")


def assistants_factory(client: AsyncOpenAI):
  storage = "tutors.yaml"

  try:
    with open(storage, 'r') as file:
      [tutors, user_prefs] = yaml.safe_load(file) or {}
  except FileNotFoundError:
    logger.warn(f"{storage} not found")
    tutors = {
        "demo": {"desc": "ai assistant", "id": "asst_fake_id"}
    }
    user_prefs = {}

  default_assistant = tutors.get("default", next(iter(tutors.values())))
  cache = {}

  async def get_assistant(user_id=None, new_tutor=None):
    if user_id is None:
      return tutors

    now = datetime.now()

    if new_tutor and new_tutor in tutors:
      assistant_id = tutors[new_tutor]["id"]
      user_prefs[user_id] = new_tutor
      cache.pop(user_id, None)
      with open(storage, 'w') as file:
        yaml.dump([tutors, user_prefs], file, allow_unicode=True)
    else:
      assistant_id = tutors.get(user_prefs.get(user_id), default_assistant)["id"]

    if user_id not in cache or (now - cache[user_id]["expire_date"]).total_seconds() > 86400:

      assistant = await client.beta.assistants.retrieve(assistant_id)
      logger.info(f"retrieve assistant: {user_id}, {assistant.id}")

      cache[user_id] = {
          "expire_date": now + timedelta(days=1),
          "assistant": assistant
      }

    return cache[user_id]["assistant"]

  return get_assistant

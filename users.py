import yaml
from .logger import create_logger
from . import env
from pathlib import Path
from aiogram import types

logger = create_logger(__name__)
allowed_users = set()
banned_users = set()


def load_users(filename):
  try:
    with open(Path(__file__).parent / filename, 'r') as file:
      return set(yaml.safe_load(file) or [-1])
  except FileNotFoundError:
    return set([-1])


def check_user(user: types.User):
  if not allowed_users:
    allowed_users.update(load_users("allowed_users.yaml"))

  if user.id not in allowed_users:
    logger.fatal(f"user '{user.username}' is not allowed, id={user.id}")
    return True

  return False


def check_group(chat_id):
  return chat_id != env.GROUP_ID


def is_user_not_allowed(message: types.Message):
  if message.from_user.is_bot:
    return True

  if hasattr(env, "GROUP_ID"):
    return check_group(message.chat.id)

  return check_user(message.from_user)


def is_user_banned(user_id):
  if not banned_users:
    banned_users.update(load_users("banned_users.yaml"))

  if user_id in banned_users:
    logger.debug(f"user is banned, id={user_id}")
    return True

  return False

import yaml
from .logger import create_logger
from . import env
from pathlib import Path
from aiogram import types

logger = create_logger(__name__)
allowed_users = set()


def load_allowed_users():
  try:
    with open(Path(__file__).parent / "allowed_users.yaml", 'r') as file:
      return set(yaml.safe_load(file) or [])
  except FileNotFoundError:
    return set()


def check_user(user: types.User):
  if not allowed_users:
    allowed_users.update(load_allowed_users())

  if user.id not in allowed_users:
    logger.fatal(f"user '{user.username}' is not allowed, id={user.id}")
    return True
  return False


def check_group(chat_id):
  return chat_id != env.GROUP_ID


def is_user_not_allowed(message: types.Message):
  if message.from_user.is_bot:
    return True

  if "GROUP_ID" in env:
    return check_group(message.chat.id)

  return check_user(message.from_user)

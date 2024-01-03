import yaml
from logger import create_logger

logger = create_logger(__name__)

try:
  with open("allowed_users.yaml", 'r') as file:
    allowed_users = yaml.safe_load(file) or {}
except FileNotFoundError:
  allowed_users = []


def check_user(user_id, username):
  if user_id not in allowed_users and allowed_users:
    logger.fatal(f"user '{username}' is not allowed, id={user_id}")
    return True
  return False

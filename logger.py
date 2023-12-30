import sys
import logging
from os import getenv

LOG_LEVEL = getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL, stream=sys.stdout)


def create_logger(module_name):
  logger = logging.getLogger(f"gptbot:{module_name}")
  return logger

import sys
import logging
from . import env

logging.basicConfig(level=env.LOG_LEVEL, stream=sys.stdout)


def create_logger(module_name):
  logger = logging.getLogger(f"gptbot:{module_name}")
  return logger

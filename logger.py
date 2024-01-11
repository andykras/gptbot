from .formatter import ColorFormatter
import logging
from . import env

logging.basicConfig(level=env.LOG_LEVEL, handlers=[ColorFormatter.get_handler()])


def create_logger(module_name):
  logger = logging.getLogger(f"gptbot:{module_name}")
  return logger

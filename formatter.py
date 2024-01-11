import logging
import re
import hashlib
import base64
from collections import defaultdict
from itertools import cycle


class ColorFormatter(logging.Formatter):
  COLOR_CODES = cycle([
      "\033[34m",   # 1. blue
      "\033[35m",   # 2. purple
      "\033[36m",   # 3. cyan
      "\033[33m",   # 4. yellow
      "\033[32m",   # 5. green
      "\033[31m",   # 6. red
      "\033[91m",   # 7. light red
      "\033[92m",   # 8. light green
      "\033[93m",   # 9. light yellow
      "\033[94m",   # 10. light blue
      "\033[95m",   # 11. light purple
      "\033[96m",   # 12. light cyan
      "\033[41m",   # 13. bg: red
      "\033[42m",   # 14. bg: green
      "\033[43m",   # 15. bg: yellow
      "\033[44m",   # 16. bg: blue
      "\033[45m",   # 17. bg: purple
      "\033[46m",   # 18. bg: cyan
      "\033[100m",  # 19. bg: dark gray
      "\033[101m",  # 20. bg: dark red
      "\033[102m",  # 21. bg: dark green
      "\033[103m",  # 22. bg: dark yellow
      "\033[104m",  # 23. bg: dark blue
      "\033[105m",  # 24. bg: dark purple
      "\033[106m",  # 25. bg: dark cyan
  ])

  MODULE_COLORS = defaultdict(lambda: next(ColorFormatter.COLOR_CODES))
  KEYWORD_COLORS = MODULE_COLORS
  URL_COLOR = "\033[94m"      # light blue
  NUMBER_COLOR = "\033[92m"   # green
  LEVEL_COLOR = "\033[33m"    # yellow
  RESET_COLOR = "\033[0m"     # color reset
  LINKS = {}
  NUMBERS = {}
  KEYWORDS = [
      "thread", "bot", "assistant", "user",
      "on_start", "process_message", "retrieve_messages", "andykras"
      "text", "status", "queued", "in_progress", "completed", "done"
  ]

  def format(self, record):
    message = record.getMessage()
    module = record.name.split(':')[0]
    color = self.MODULE_COLORS[module]

    level = f"{self.LEVEL_COLOR}{record.levelname}{self.RESET_COLOR}"
    module = f"{color}{module}{self.RESET_COLOR}"

    message = re.sub(r"https?://[\w./-]+", lambda match: self._replace_link(match), message)
    message = re.sub(r"(\d+)", lambda match: self._replace_number(match), message)

    for keyword in self.KEYWORDS:
      message = re.sub(rf"({keyword})", f"{self.KEYWORD_COLORS[keyword]}\\1{self.RESET_COLOR}", message)

    message = self._restore_links(message)
    message = self._restore_numbers(message)

    return f"{level}:{module}:{message}"

  def get_hash(self, data):
    base64_encoded = base64.b64encode(hashlib.sha1(data.encode()).digest()).decode()

    vocabulary = str.maketrans(
        "0123456789+/=",
        "ABCDEFGHIJKLM"
    )

    return base64_encoded.translate(vocabulary)

  def _replace_link(self, match):
    link = f"{self.URL_COLOR}{match.group(0)}{self.RESET_COLOR}"
    link_hash = self.get_hash(link)
    self.LINKS[link_hash] = link
    return link_hash

  def _restore_links(self, message):
    for link_hash, link in self.LINKS.items():
      message = message.replace(link_hash, link)
    return message

  def _replace_number(self, match):
    number = f"{self.NUMBER_COLOR}{match.group(0)}{self.RESET_COLOR}"
    number_hash = self.get_hash(number)
    self.NUMBERS[number_hash] = number
    return number_hash

  def _restore_numbers(self, message):
    for number_hash, number in self.NUMBERS.items():
      message = message.replace(number_hash, number)
    return message

  @classmethod
  def get_handler(cls):
    handler = logging.StreamHandler()
    handler.setFormatter(cls())
    return handler

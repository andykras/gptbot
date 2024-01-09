from locale import getdefaultlocale
from .messages import messages
from .logger import create_logger

logger = create_logger(__name__)

lang = getdefaultlocale()[0]
lang = lang if lang in messages else "en_US"
translations = messages[lang]


def _t(path, **kwargs):
  keys = path.split('.')
  translation = translations
  for key in keys:
    if key not in translation:
      logger.error(f"missing translation: {path}")
      return f"`{path}`"
    translation = translation[key]

  return translation.format(**kwargs)

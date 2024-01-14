from os import getenv

# envirionments (or define here)
LOG_LEVEL = getenv("LOG_LEVEL", "INFO").upper()
BOT_TOKEN = getenv("BOT_TOKEN")
ORG_ID = getenv("ORG_ID")
API_KEY = getenv("API_KEY")

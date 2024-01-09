from os import getenv

# envirionments (or define here)
LOG_LEVEL = getenv("LOG_LEVEL", "INFO").upper()
BOT_TOKEN = getenv("BOT_TOKEN")
ORG_ID = getenv("ORG_ID")
API_KEY = getenv("API_KEY")

# settings
# GROUP_ID = -123123 # set this if you want bot to work in chats\groups
THREADS_RUN_POLLING_TIMEOUT = 1  # in seconds

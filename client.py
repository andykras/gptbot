from os import getenv
from openai import AsyncOpenAI
from thread_factory import thread_factory
from assistants_factory import assistants_factory

ORG_ID = getenv("ORG_ID")
API_KEY = getenv("API_KEY")

client = AsyncOpenAI(api_key=API_KEY, organization=ORG_ID)
get_thread = thread_factory(client)
get_assistant = assistants_factory(client)

import env
from openai import AsyncOpenAI
from thread_factory import thread_factory
from assistants_factory import assistants_factory

client = AsyncOpenAI(api_key=env.API_KEY, organization=env.ORG_ID)
get_thread = thread_factory(client)
get_assistant = assistants_factory(client)

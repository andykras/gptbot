from . import env
from openai import AsyncOpenAI
from .threads_factory import threads_factory
from .assistants_factory import assistants_factory

client = AsyncOpenAI(api_key=env.API_KEY, organization=env.ORG_ID)
get_thread = threads_factory(client)
get_assistant, asst_filter = assistants_factory(client)

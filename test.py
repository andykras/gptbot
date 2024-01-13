import pytest
import time
import asyncio
from datetime import datetime, timedelta
from freezegun import freeze_time
from unittest.mock import MagicMock, AsyncMock, patch, mock_open
from pathlib import Path
from .threads_factory import threads_factory
from .assistants_factory import assistants_factory
from .message_queues import QueueController, thread_lock


def load_mock_data(file_name):
  with open(Path(__file__).parent / "mock" / file_name, 'r') as file:
    return file.read()


mock_threads_yaml = load_mock_data("threads.yaml")
mock_tutors_yaml = load_mock_data("tutors.yaml")
mock_allowed_users = load_mock_data("allowed_users.yaml")


mock_client = AsyncMock()
mock_client.beta.assistants.retrieve = AsyncMock(side_effect=lambda assistant_id: AsyncMock(id=assistant_id))
mock_client.beta.threads.create = AsyncMock(return_value=AsyncMock(id="new_thread_id"))
mock_client.beta.threads.retrieve = AsyncMock(return_value=AsyncMock(id="existing_thread_id"))
get_thread = threads_factory(mock_client)
get_assistant, asst_filter = assistants_factory(mock_client)


@pytest.mark.asyncio
async def test_retrieve_existing_thread():
  with patch("builtins.open", mock_open(read_data=mock_threads_yaml)):
    existing_thread = await get_thread(123)
    assert existing_thread.id == "existing_thread_id"
    mock_client.beta.threads.retrieve.assert_called_with("old_thread_id")


@pytest.mark.asyncio
async def test_clear_context():
  with patch("builtins.open", mock_open(read_data=mock_threads_yaml)):
    new_thread = await get_thread(123, new_thread=True)
    assert new_thread.id == "new_thread_id"
    mock_client.beta.threads.create.assert_called()


@pytest.mark.asyncio
async def test_cache_thread_expiration():
  with patch("builtins.open", mock_open(read_data=mock_threads_yaml)):
    with freeze_time(datetime.now() + timedelta(days=2)):
      await get_thread(123)
      mock_client.beta.threads.retrieve.assert_called()


@pytest.mark.asyncio
async def test_create_thread_for_new_user():
  with patch("builtins.open", mock_open(read_data=mock_threads_yaml)):
    new_user_thread = await get_thread(456)
    assert new_user_thread.id == "new_thread_id"
    mock_client.beta.threads.create.assert_called()


@pytest.mark.asyncio
async def test_get_list_of_assistants():
  with patch("builtins.open", mock_open(read_data=mock_tutors_yaml)):
    tutors = await get_assistant()
    assert isinstance(tutors, dict)


@pytest.mark.asyncio
async def test_get_current_assistant():
  with patch("builtins.open", mock_open(read_data=mock_tutors_yaml)):
    assistant = await get_assistant(user_id=123)
    assert assistant.id == "asst_id2_from_openai"


@pytest.mark.asyncio
async def test_change_assistant():
  with patch("builtins.open", mock_open(read_data=mock_tutors_yaml)):
    new_assistant = await get_assistant(user_id=123, new_tutor="default")
    assert new_assistant.id == "asst_id1_from_openai"


@pytest.mark.asyncio
async def test_defaults():
  with patch("builtins.open", mock_open(read_data="")) as mock_tutors_file:
    tutors = await get_assistant()
    tutors.clear()  # force to reload
    tutors = await get_assistant()
    assert "default" in tutors
    assert tutors["default"]["id"] == "asst_id_from_openai"
    mock_tutors_file.assert_called_with(Path(__file__).parent / "tutors.yaml", 'r')


@pytest.mark.parametrize("user_id, expected", [
    (123, True),
    (456, True),
    (789, False),
])
def test_check_allowed_users(user_id, expected):
  with patch("builtins.open", mock_open(read_data=mock_allowed_users)):
    from .users import check_user
    from collections import namedtuple
    UserMock = namedtuple("UserMock", ["id", "username"])
    assert not check_user(UserMock(id=user_id, username=user_id)) == expected


class MsgBuilder:
  def __init__(self):
    self.messages = []
    self.count = {}

  def user(self, user_id):
    self.count[user_id] = self.count.get(user_id, 0) + 1
    text = f"user{user_id} say {self.count[user_id]}"
    self.messages.append({"text": text, "user_id": user_id})
    return self

  def build(self):
    return self.messages


def create_messages(user_map, messages_data):
  return [{"text": msg_data["text"], "user": user_map[msg_data["user_id"]]} for msg_data in messages_data]


def get_expected_texts_by_order(messages, order):
  texts_by_user = {user.id: [] for user in order}
  for msg in messages:
    texts_by_user[msg["user"].id].append(msg["text"])
  expected_texts = []
  for user in order:
    expected_texts.extend(texts_by_user[user.id])
  return expected_texts


async def run_test_with_order_and_messages(user_order, messages):
  add_messages_to_thread = AsyncMock()
  process_message = AsyncMock()

  thread = MagicMock(id="shared_thread")
  delta = 0.01

  async def handle_response(message):
    if not QueueController.start_queue(thread, message["mock"]):
      return

    await QueueController.wait_next(delta, thread, message["user"].id)
    async with thread_lock(thread.id, message["user"].id) as messages:
      await add_messages_to_thread(thread, messages)
      await process_message(thread, MagicMock(), messages[-1])

  current_time = time.time() + delta
  for msg in messages:
    msg["mock"] = MagicMock(from_user=msg["user"], text=msg["text"])
    msg["mock"].date.timestamp.return_value = current_time
    current_time += delta

  tasks = [asyncio.create_task(handle_response(msg)) for msg in messages]
  await asyncio.gather(*tasks)

  expected_texts = get_expected_texts_by_order(messages, user_order)
  actual_texts = [msg.text for call in add_messages_to_thread.call_args_list for msg in call[0][1]]

  assert actual_texts == expected_texts
  assert process_message.call_count == 2  # total users


@pytest.mark.asyncio
@pytest.mark.parametrize("users, messages_data", [
    ([MagicMock(id=1), MagicMock(id=2)], MsgBuilder().user(1).user(2).user(1).user(1).user(2).build()),
    ([MagicMock(id=2), MagicMock(id=1)], MsgBuilder().user(1).user(2).user(1).user(2).user(1).build())
],
    ids=["order: user1, user2", "order: user2, user1"])
async def test_multiple_requests(users, messages_data):
  user_map = {user.id: user for user in users}
  messages = create_messages(user_map, messages_data)
  await run_test_with_order_and_messages(users, messages)

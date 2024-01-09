import pytest
from datetime import datetime, timedelta
from freezegun import freeze_time
from unittest.mock import AsyncMock, patch, mock_open
from pathlib import Path
from .threads_factory import threads_factory
from .assistants_factory import assistants_factory


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


@pytest.mark.parametrize("user_id,expected", [
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

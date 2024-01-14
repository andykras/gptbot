import time
from enum import Enum
from aiogram import types


def get_unclosed_tag(markdown):
  tags = ["```", "`", "*", "_"]
  current_tag = ""

  i = 0
  while i < len(markdown):
    if markdown[i] == '\\' and current_tag == "":
      i += 2
      continue
    if current_tag != "":
      if markdown[i:].startswith(current_tag):
        i += len(current_tag)
        current_tag = ""
        continue
    else:
      for tag in tags:
        if markdown[i:].startswith(tag):
          current_tag = tag
          i += len(current_tag)
          break
    i += 1

  return current_tag


def is_valid_markdown(markdown):
  return get_unclosed_tag(markdown) == ""


def escape_markdown(text):
  special_chars = ["*", "_", "`"]

  for char in special_chars:
    open_tags = text.count(char) % 2 != 0
    if open_tags:
      text = text.replace(char, "\\" + char)

  return text


class ChatActions:
  last_sent_time = {}

  class Action(Enum):
    TYPING = "typing"
    UPLOAD_PHOTO = "upload_photo"
    RECORD_VIDEO = "record_video"
    UPLOAD_VIDEO = "upload_video"
    RECORD_VOICE = "record_voice"
    UPLOAD_VOICE = "upload_voice"
    UPLOAD_DOCUMENT = "upload_document"
    FIND_LOCATION = "find_location"
    RECORD_VIDEO_NOTE = "record_video_note"
    UPLOAD_VIDEO_NOTE = "upload_video_note"

  @classmethod
  async def send(cls, message: types.Message, action: Action = Action.TYPING):
    current_time = time.time()
    chat_id = message.chat.id

    if chat_id not in cls.last_sent_time or current_time - cls.last_sent_time[chat_id] > 5:
      await message.bot.send_chat_action(chat_id, action)
      cls.last_sent_time[chat_id] = current_time

  @classmethod
  async def send_typing(cls, message: types.Message):
    await cls.send(message, cls.Action.TYPING)

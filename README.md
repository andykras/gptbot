# ChatGPT Telegram Bot

<div align="center">
  <img src="tg.jpg" alt="GPT Bot Image">
</div>

## Overview

This project is a Telegram bot leveraging the new Assistance API of OpenAI to integrate the conversational intelligence of ChatGPT into Telegram. Utilizing the AsyncOpenAI client, it allows users to interact with a GPT-powered assistant directly through Telegram messages, providing a seamless and efficient experience.

## Dependencies

To use this bot, you will need to set up a few things:

- **OpenAI API Key**: Create an API key at [OpenAI Platform](https://platform.openai.com/api-keys).
- **Assistant**: Create a new assistant at [OpenAI Assistants](https://platform.openai.com/assistants). You will need to note the assistant ID to configure in either `tutors.yaml` or `assistants_factory.py`.
- **Telegram Bot**: Create a new bot on Telegram via [BotFather](https://t.me/BotFather) and keep the bot token.

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/andykras/gptbot.git
```

2. **Install required packages:**

```bash
pip install -r requirements.txt
```

3. **Set environment variables:**

```bash
export LOG_LEVEL=INFO
export ORG_ID="org-..."
export API_KEY="sk-..."
export BOT_TOKEN="..."
```

4. **Prepare YAML files:**
   - `allowed_users.yaml`: Optional, add this file to restrict access to your ChatGPT bot.
   - `threads.yaml`: Will be created by the bot.
   - `tutors.yaml`: Will be created by the bot; ensure a valid default is set in `assistants_factory.py`.

## Running the Bot

To start the bot, run:

```bash
python gptbot.py
```

Interact with your ChatGPT bot via Telegram and enjoy conversing with AI!

## Notes

- Ensure all prerequisites are met and environment variables are set before starting the bot.
- Modify `allowed_users.yaml`, `threads.yaml`, and `tutors.yaml` as needed to customize the bot's behavior.


```bash
$ LC_ALL=ru_RU python gptbot.py | lolcat
INFO:aiogram.dispatcher:Start polling
INFO:aiogram.dispatcher:Run polling for bot @*****bot id=******* - 'ChatGPT 3.5'
INFO:httpx:HTTP Request: GET https://api.openai.com/v1/assistants/asst_******** "HTTP/1.1 200 OK"
INFO:users:retrieve assistant: *******, asst_********
INFO:actions:new_assistant:*******:default:asst_********
INFO:aiogram.event:Update id=96266759 is handled. Duration 5218 ms by bot id=*******
INFO:actions:user:*******:*******
        привет!
INFO:httpx:HTTP Request: GET https://api.openai.com/v1/threads/thread_27HpnQYhVZ9K9T5eMWsXe8y0 "HTTP/1.1 200 OK"
INFO:users:retrieve thread: *******, thread_27HpnQYhVZ9K9T5eMWsXe8y0
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/threads/thread_27HpnQYhVZ9K9T5eMWsXe8y0/messages "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/threads/thread_27HpnQYhVZ9K9T5eMWsXe8y0/runs "HTTP/1.1 200 OK"
INFO:actions:status:queued
INFO:httpx:HTTP Request: GET https://api.openai.com/v1/threads/thread_27HpnQYhVZ9K9T5eMWsXe8y0/runs/run_3pZQzNZZtDWGFrcQsEiTG9G3 "HTTP/1.1 200 OK"
INFO:actions:status:completed
INFO:httpx:HTTP Request: GET https://api.openai.com/v1/threads/thread_27HpnQYhVZ9K9T5eMWsXe8y0/runs/run_3pZQzNZZtDWGFrcQsEiTG9G3/steps "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: GET https://api.openai.com/v1/threads/thread_27HpnQYhVZ9K9T5eMWsXe8y0/messages/msg_HSDxxZ1DPW5JSnoeAo21msOU "HTTP/1.1 200 OK"
INFO:actions:assistant:asst_********:
        Привет, ******! Чем могу помочь?
INFO:actions:done
INFO:aiogram.event:Update id=96266760 is handled. Duration 3059 ms by bot id=*******
```
# Multibot Deployment Guide

This guide will help you set up a multi-bot environment using Python and the Aiogram library. You will create a directory structure to manage multiple Telegram bots and use a single script, `multibot.py`, to run and control them.

## Directory Structure

Start by organizing your project into the following directory structure:

```
project/
├── gptbot1/
│   ├── cd gptbot1
│   ├── git clone https://github.com/andykras/gptbot.git .
│   └── Clone or add your first bot's code here
│
├── gptbot2/
│   ├── cd gptbot2
│   ├── git clone https://github.com/andykras/gptbot.git .
│   └── Clone or add your second bot's code here
│
└── multibot.py
```

- `project/`: The root dir of your project.
- `gptbot1/`: Dir for your first bot.
- `gptbot2/`: Dir for your second bot.
- `multibot.py`: Put this file above bot folders.

## Code Setup

1. Clone or add your bot code into the respective bot directories (`gptbot1/`, `gptbot2/`, etc.). Ensure that each bot has its own unique code and configurations.

2. Setup your BOT_TOKENs, API_KEYs, etc. You will need to manually configure them in the `env.py` file. Since the bots share a common environment, you should set these variables manually in the `env.py` file for proper configuration.

3. Run bots:

```bash
cd project
python multibot.py
```

`multibot.py` script will initialize and manage all the configured bots concurrently.

4. To stop the multi-bot system, press `Ctrl+C` in the terminal.

This setup allows you to run and manage multiple Telegram bots within a single project, making it easier to develop and control them.

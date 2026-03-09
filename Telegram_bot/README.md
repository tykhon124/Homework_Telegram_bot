# Homework Telegram Bot

# Did by Tykhon Liamtsev

## Description

This project is a Telegram bot created using the aiogram framework.
The bot helps students manage homework tasks.

Users can:

* add tasks
* view tasks
* search tasks by subject
* delete tasks

## Technologies

* Python
* aiogram
* asyncio

## Installation

1. Clone repository

2. Create virtual environment

```
python -m venv venv
```

3. Activate environment

Windows:

```
venv\Scripts\activate
```

Linux / Mac:

```
source venv/bin/activate
```

4. Install dependencies

```
pip install -r requirements.txt
```

## Configuration

Add your Telegram bot token to:

```
config.py
```

Example:

```
TOKEN = "YOUR_BOT_TOKEN"
```

## Run bot

```
python bot.py
```

## Commands

/start – start bot
/add – add new task
/show_notice – show tasks
/delete_notice – delete task
/search – search task by subject


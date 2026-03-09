import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        handlers=[
            logging.FileHandler("bot_logger.log", mode="a", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

# commands.py - модуль в якому оголошені всі необхідні команди(та їх фільтри)
from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

"""Command to create bot commands"""

logging.info("Commands loading")
START_COMMAND = Command('start')
SHOW_NOTICE_COMMAND = Command('show_notice',)
ADD_COMMAND = Command('add')
DELETE_COMMAND = Command('delete_notice')
SEARCH_COMMAND = Command('search')
CANCEL_COMMAND = Command('cancel')


ADD_BOT_COMMAND = BotCommand(command='add', description="Add notice")
DELETE_BOT_COMMAND = BotCommand(command='delete_notice', description="Delete notice")
START_BOT_COMMAND = BotCommand(command='start', description="Start bot")
SHOW_NOTICE_BOT_COMMAND = BotCommand(command='show_notice', description="Show notice text")
SEARCH_BOT_COMMAND = BotCommand(command='search', description="Search bot")
CANCEL_BOT_COMMAND = BotCommand(command='cancel', description="Cancel")
list_hint_commands = [ADD_BOT_COMMAND, DELETE_BOT_COMMAND, START_BOT_COMMAND, SHOW_NOTICE_BOT_COMMAND, SEARCH_BOT_COMMAND]
logger.info("Commands loaded")
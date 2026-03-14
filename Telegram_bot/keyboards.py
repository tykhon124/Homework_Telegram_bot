import logging

logger = logging.getLogger(__name__)

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def create_main_keyboard():
    """Create main keyboard"""
    logger.info("Keyboard creating...")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Add task"), KeyboardButton(text="📋 Show tasks")],
            [KeyboardButton(text="❌ Delete task"), KeyboardButton(text="🔎 Search task")],
            [KeyboardButton(text="🔙 Cancel")]
        ],
        resize_keyboard=True
    )
    logger.info("Keyboard created")
    return keyboard


def create_days_keyboard():
    """Create days keyboard"""
    logger.info("Days_Keyboard creating...")
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Monday", callback_data="day_monday"),
                InlineKeyboardButton(text="Tuesday", callback_data="day_tuesday")
            ],
            [
                InlineKeyboardButton(text="Wednesday", callback_data="day_wednesday"),
                InlineKeyboardButton(text="Thursday", callback_data="day_thursday")
            ],
            [
                InlineKeyboardButton(text="Friday", callback_data="day_friday")
            ]
        ]
    )
    logger.info("Days_Keyboard created")
    return keyboard

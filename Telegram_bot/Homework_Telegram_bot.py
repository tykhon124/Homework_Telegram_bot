import logging
import asyncio

logger = logging.getLogger(__name__)

logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        handlers=[
            logging.FileHandler("bot_logger.log", mode="a", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )


# ===================== AIOGRAM =====================
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

# ===================== LOCAL FILES =====================
from config import TOKEN
from models import Notice
from data import add_notice, get_notices_for_user, delete_notice, read_user_data
from state import HomeworkForm
from keyboards import create_main_keyboard, create_days_keyboard


def async_log_function_call(func):
   """Decorator for logging asynchronous function calls"""
   from functools import wraps
   @wraps(func)
   async def wrapper(*args, **kwargs):
        logger.info(f"Function called {func.__name__}")

        try:
            result = await func(*args, **kwargs)
            logger.info(f"Function finished: {func.__name__}")
            return result

        except Exception as e:
            logger.exception(f"Error in: {func.__name__}: {e}")
            raise

   return wrapper


# ===================== INIT =====================

dp = Dispatcher()

# =====================================================
# START / MENU
# =====================================================

@dp.message(Command("start"))
@async_log_function_call
async def command_start_handler(message: Message):
    """Command handler for start command"""
    logger.info(f"User {message.from_user.id} started bot")
    await message.answer(
        f"Hello, {message.from_user.first_name} 👋",
        reply_markup=create_main_keyboard()
    )
    logger.info("Start Command finished")


@dp.message(Command("show"))
@async_log_function_call
async def command_show_handler(message: Message):
    """Command handler for show command"""
    logger.info("Show Command calling")
    await message.answer(
        "Choose what you need:",
        reply_markup=create_main_keyboard()
    )
    logger.info("Show Command finished")


# =====================================================
# Cancel
# =====================================================


@dp.message(Command("cancel"))
@dp.message(F.text.in_(["cancel", "🔙 Cancel", "exit"]))
@async_log_function_call
async def command_cancel(message: Message, state: FSMContext):
    """Command handler for cancel command"""
    current_state = await state.get_state()

    if current_state is None:
        await message.answer("Nothing to cancel")
        return

    await state.clear()
    await message.answer("❌ Operation cancelled.", reply_markup=create_main_keyboard())


@dp.callback_query(F.data == "cancel")
async def cancel_callback(callback: CallbackQuery, state: FSMContext):
    """Callback handler for cancel command"""
    await callback.answer()
    await state.clear()

    await callback.message.answer("❌ Operation cancelled.", reply_markup=create_main_keyboard())


# =====================================================
# ADD NOTICE
# =====================================================

@dp.message(Command("add"))
@async_log_function_call
async def command_add_handler(message: Message, state: FSMContext):
    """Command handler for add command"""
    logger.info(f"User {message.from_user.id} used /add")
    await state.clear()
    await message.answer(
        "Choose a day:",
        reply_markup=create_days_keyboard()
    )
    await state.set_state(HomeworkForm.select_day)


@dp.callback_query(F.data.startswith("day_"))
async def choose_day_handler(callback: CallbackQuery, state: FSMContext):
    """Callback handler for choose day"""
    await callback.answer()

    selected_day = callback.data.split("_")[1]
    await state.update_data(day=selected_day)

    await callback.message.answer(
        "Enter subject:",
        reply_markup=create_main_keyboard()
    )

    await state.set_state(HomeworkForm.select_subject)

@dp.message(HomeworkForm.select_day, F.text)
async def wrong_day_input(message: Message):
    """Handler for wrong day input"""
    await message.answer("❌ Please select a day: ",)


@dp.message(HomeworkForm.select_subject, F.text)
@async_log_function_call
async def select_subject_handler(message: Message, state: FSMContext):
    """Callback handler for select subject"""
    await state.update_data(subject=message.text)
    await message.answer("Enter task description:")
    await state.set_state(HomeworkForm.select_writing_task)


@dp.message(HomeworkForm.select_writing_task, F.text.len() > 3)
@async_log_function_call
async def select_task_handler(message: Message, state: FSMContext):
    """Callback handler for select task"""
    await state.update_data(w_task=message.text)

    data = await state.get_data()
    data["user_id"] = str(message.from_user.id)

    task = Notice(**data)
    add_notice(task)
    logger.info(f"User {message.from_user.id} added task {task.subject}")

    await state.clear()
    await message.answer("✅ Task saved!", reply_markup=create_main_keyboard())
    logger.info("Add Command finished")

@dp.message(HomeworkForm.select_writing_task)
async def task_error(message: Message):
    """Callback handler for task error"""
    await message.answer("❌ Task too short!\n" "Please enter a normal item name.")


# =====================================================
# SHOW NOTICE
# =====================================================

@dp.message(Command("show_notice"))
@async_log_function_call
async def show_notice_handler(message: Message):
    """Command handler for show notice"""
    logger.info(f"User {message.from_user.id} requested tasks")
    user_id = str(message.from_user.id)
    notices = get_notices_for_user(user_id)

    if not notices:
        await message.answer("📭 You don't have any notes.")
        return

    text = "📚 <b>Your tasks:</b>\n\n"

    for i, notice in enumerate(notices, start=1):
        text += (
            f"{i}. 📅 {notice['day'].capitalize()}\n"
            f"   📖 {notice['subject']}\n"
            f"   📝 {notice['w_task']}\n\n"
        )

    await message.answer(text, reply_markup=create_main_keyboard())
    logger.info("Show Notice finished")


# =====================================================
# SEARCH
# =====================================================

@dp.message(Command("search"))
@async_log_function_call
async def start_search(message: Message):
    """Command handler for start search"""
    user_id = str(message.from_user.id)
    tasks = read_user_data(user_id)

    if not tasks:
        await message.answer("You don't have any tasks.")
        return

    subject = list({task["subject"] for task in tasks})

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=sub, callback_data=f"subject_{sub}")]
            for sub in subject
        ]
    )
    await message.answer("📚 Choose subject:", reply_markup=keyboard)


@dp.callback_query(F.data.startswith("subject_"))
@async_log_function_call
async def search_handler(callback: CallbackQuery):
    """Callback handler for search"""
    await callback.answer()

    subject = callback.data.split("_", 1)[1].lower()
    user_id = str(callback.from_user.id)

    tasks = read_user_data(user_id)

    results = [
        task for task in tasks
        if task["subject"].lower() == subject.lower()
    ]

    if not results:
        await callback.message.answer("Nothing found.")
        return

    text = "<b>Found tasks:</b>\n\n"

    for task in results:
        text += (
            f"📅 {task['day'].capitalize()}\n"
            f"📖 {task['subject']}\n"
            f"📝 {task['w_task']}\n\n"
        )

    await callback.message.answer(text)
    logger.info("Search Task finished")

# =====================================================
# DELETE
# =====================================================

@dp.message(Command("delete_notice"))
@async_log_function_call
async def command_delete_handler(message: Message, state: FSMContext):
    """Command handler for delete notice"""
    logger.info(f"User {message.from_user.id} wants to delete task")
    await state.clear()
    user_id = str(message.from_user.id)
    notices = get_notices_for_user(user_id)

    if not notices:
        await message.answer("📭 No notes to delete.")
        return

    text = "Choose number to delete:\n\n"

    for i, notice in enumerate(notices, start=1):
        text += f"{i}. {notice['subject']} - {notice['w_task']}\n"

    text += "\nType number or press Cancel"

    await message.answer(text, reply_markup=create_main_keyboard())
    await state.set_state(HomeworkForm.select_delete_index)


@dp.message(HomeworkForm.select_delete_index)
@async_log_function_call
async def delete_notice_handler(message: Message, state: FSMContext):
    """Command handler for delete notice by index"""
    user_id = str(message.from_user.id)
    notices = get_notices_for_user(user_id)

    try:
        index = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Enter a number.\nExample: 1, 2 ,3")
        return

    if index < 1 or index > len(notices):
        await message.answer(f"❌ Enter number from 1 to {len(notices)}")
        return

    delete_notice(user_id, index - 1)

    await message.answer("✅ Deleted.", reply_markup=create_main_keyboard())
    logger.info("Delete Notice finished")
    await state.clear()


# =====================================================
# MAIN
# =====================================================

async def main():
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    await dp.start_polling(bot)

@dp.message(F.text == "➕ Add task")
async def add_from_button(message: Message, state: FSMContext):
    await command_add_handler(message, state)


@dp.message(F.text == "📋 Show tasks")
async def show_from_button(message: Message):
    await show_notice_handler(message)


@dp.message(F.text == "❌ Delete task")
async def delete_from_button(message: Message, state: FSMContext):
    await command_delete_handler(message, state)


@dp.message(F.text == "🔎 Search task")
async def search_from_button(message: Message):
    await start_search(message)

@dp.message(F.text == "🔙 Cancel")
async def cancel_from_button(message: Message, state: FSMContext):
    await command_cancel(message, state)

@dp.message(StateFilter(None))
async def unknown_command(message: Message):
    await message.answer("I don't understand you. Use menu buttons.", reply_markup=create_main_keyboard())

if __name__ == "__main__":
    asyncio.run(main())
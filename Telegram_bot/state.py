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

from aiogram.fsm.state import State, StatesGroup

class HomeworkForm(StatesGroup):
    """Homework form state"""
    select_day = State()
    select_subject = State()
    select_writing_task = State()
    select_delete_index = State()
    logger.info("Homework Form Created")

class SearchTaskForm(StatesGroup):
    """Search task form state"""
    subject_query = State()
    logger.info("Search Task Form Created")
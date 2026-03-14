import logging

logger = logging.getLogger(__name__)

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

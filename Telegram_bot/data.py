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

import json
import os
from models import Notice

FILE_PATH = "homework_data.json"


# =============================
# HELPERS
# =============================

def load_data():
    """Load data from json file"""
    if not os.path.exists(FILE_PATH):
        logging.warning("Json file not found, creating new one")
        return {}

    with open(FILE_PATH, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            logger.error("Json decoding error")
            return {}


def save_data(data):
    """Save data to json file"""
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        logger.info(f"Data save {FILE_PATH}")


# =============================
# CRUD
# =============================

def add_notice(notice: Notice):
    """Add notice to database"""
    data = load_data()

    user_id = notice.user_id

    if user_id not in data:
        logging.warning("No user id")
        data[user_id] = []

    data[user_id].append({
        "day": notice.day,
        "subject": notice.subject,
        "w_task": notice.w_task,
    })
    logger.info("Notice added")
    save_data(data)


def get_notices_for_user(user_id: str):
    """Get notices for user"""
    data = load_data()
    logger.info("Notice got for user")
    return data.get(user_id, [])


def delete_notice(user_id: str, index: int):
    """Delete notice"""
    data = load_data()

    if user_id not in data:
        logger.warning("No user id")
        return False

    if index < 0 or index >= len(data[user_id]):
        return False

    data[user_id].pop(index)
    save_data(data)
    return True


def read_user_data(user_id: str):
    """Read user data"""
    data = load_data()
    logger.info("User id read")

    return data.get(user_id, [])

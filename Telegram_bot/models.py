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

from pydantic import BaseModel

class Notice(BaseModel):
    """Create notice model"""
    user_id: str
    subject: str
    w_task: str
    day: str
    logger.info("Model Notice finished")
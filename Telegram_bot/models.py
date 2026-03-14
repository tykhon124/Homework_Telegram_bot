import logging

logger = logging.getLogger(__name__)

from pydantic import BaseModel

class Notice(BaseModel):
    """Create notice model"""
    user_id: str
    subject: str
    w_task: str
    day: str
    logger.info("Model Notice finished")

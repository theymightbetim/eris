from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def is_it_wednesday():
    """
    check if today is wednesday
    :return:
    """
    if datetime.today().weekday() == 2:
        logger.info("It's Wednesday!")
        return True
    logger.info("It's not Wednesday.")
    return False
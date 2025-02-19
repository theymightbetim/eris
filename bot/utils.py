import logging


logger = logging.getLogger(__name__)


def is_it_wednesday(date):
    """
    check if today is wednesday
    :return:
    """
    if date.weekday() == 2:
        logger.info("It's Wednesday!")
        return True
    logger.info("It's not Wednesday.")
    return False


if __name__ == "__main__":
    from subprocess import Popen, PIPE
    with Popen(['pytest',
                '__tests__/test_utils.py'],
               stdout=PIPE,
               bufsize=1,
               universal_newlines=True) as p:
        for line in p.stdout:
            print(line, end='')

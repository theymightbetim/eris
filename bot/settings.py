import pathlib
import os
import logging

path = pathlib.Path(os.path.abspath(__file__))
ROOT_DIR = path.parent.parent
LOG_PATH = os.path.join(ROOT_DIR, 'bot.log')
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)
import bot.settings as config
import requests
from datetime import date
import logging
import os


logger = logging.getLogger(__name__)

'''
Grab the new releases for this week, dump them into a file and return the file name
'''

class NewReleases:
    def __init__(self):
        self.date = date.today()
        self.url = f'https://www.previewsworld.com/NewReleases/Export?format=txt&releaseDate={self.date.strftime("%m/%d/%Y")}'
        self.filename = f"files/new-comics-{self.date.strftime('%m-%d-%y')}.txt"

    def get_new_releases(self):
        file_path = os.path.join(config.ROOT_DIR, self.filename)
        if os.path.exists(file_path) and file_path.endswith('.txt.'):
            return self.filename
        response = requests.get(self.url)
        if not response:
            return False
        if response.text != '':
            try:
                lines = str(response.text).split('\n')
                with open(file_path, 'w') as f:
                    for line in lines:
                        f.write(line)
                logging.info(f'New Releases Saves to {self.filename}')
                return self.filename
            except Exception as e:
                logging.error(e)
                return False


if __name__ == "__main__":
    from subprocess import Popen, PIPE
    with Popen(['pytest',
                '__tests__/test_comics.py'],
               stdout=PIPE,
               bufsize=1,
               universal_newlines=True) as p:
        for line in p.stdout:
            print(line, end='')
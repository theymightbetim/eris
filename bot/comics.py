import requests
from datetime import date
import logging

logger = logging.getLogger(__name__)
'''
Grab the new releases for this week, dump them into a file and return the file name
'''

class NewReleases:
    def __init__(self):
        self.date = date.today()
        self.url = f'https://www.previewsworld.com/NewReleases/Export?format=txt&releaseDate={self.date.strftime("%m/%d/%Y")}'
        self.filename = filename = f"files/new-comics-{self.date.strftime('%m-%d-%y')}.txt"

    def get_new_releases(self):
        response = requests.get(self.url)
        if response.text != '':
            try:
                lines = str(response.text).split('\n')
                with open(self.filename, 'w') as f:
                    for line in lines:
                        f.write(line)
                logging.info(f'New Releases Saves to {self.filename}')
                return self.filename
            except Exception as e:
                logging.error(e)

import requests
from datetime import date
import json

def get_todays_new_comics():
    today = date.today()
    format=today.strftime("%m/%d/%Y")
    print(format)

    url = f'https://www.previewsworld.com/NewReleases/Export?format=txt&releaseDate={format}'
    response = requests.get(url)
    if response.text != '':
        lines = str(response.text).split('\n')
        with open('files/comics.txt', 'w') as f:
            for line in lines:
                f.write(line)

import requests
from datetime import date


def get_todays_new_comics():
    today = date.today()
    formatted = today.strftime("%m/%d/%Y")
    file_format = today.strftime('%m-%d-%y')
    filename = f'files/comics-{file_format}.txt'
    url = f'https://www.previewsworld.com/NewReleases/Export?format=txt&releaseDate={formatted}'
    response = requests.get(url)
    if response.text != '':
        lines = str(response.text).split('\n')
        with open(filename, 'w') as f:
            for line in lines:
                f.write(line)
    return filename

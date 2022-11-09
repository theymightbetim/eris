import requests
from datetime import date
def get_todays_new_comics():
    today = date.today()
    format=today.strftime("%m/%d/%Y")
    fileformat=today.strftime('%m-%d-%y')
    filename = f'files/comics-{fileformat}.txt'
    url = f'https://www.previewsworld.com/NewReleases/Export?format=txt&releaseDate={format}'
    response = requests.get(url)
    if response.text != '':
        lines = str(response.text).split('\n')
        with open(filename, 'w') as f:
            for line in lines:
                f.write(line)
    return filename

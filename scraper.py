import json

import requests
from bs4 import BeautifulSoup


url = (
    'https://www.chromium.org'
    '/chromium-os/developer-information-for-chrome-os-devices'
    )

def get_as_json():
    with open('example.html', 'r') as example:
        soup = BeautifulSoup(example, 'html.parser')
    
    #page = requests.get(url)
    #soup = BeautifulSoup(page.text, 'html.parser')

if __name__ == '__main__':
    pass

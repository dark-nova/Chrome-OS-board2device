import json

import requests
from bs4 import BeautifulSoup


url = (
    'https://www.chromium.org'
    '/chromium-os/developer-information-for-chrome-os-devices'
    )

file = 'boardnamedevices.json'

model = 'Model'
bnames = 'Board name(s)'

def parse_header(header):
    """Parses header to extract `Model` and `Board name(s)` positions.

    Args:
        header (bs4.element.ResultSet): the table header with at least
            'Model' and 'Board name(s)' columns

    Returns:
        dict: 0-based indices of the columns we want

    """
    idx = {}
    in_text = [td.get_text(strip=True) for td in header]
    idx[model] = in_text.index(model)
    idx[bnames] = in_text.index(bnames)
    return (idx_model, idx_bnames)


def get_as_json():
    """Gets info as json."""
    _json = {}

    with open('example.html', 'r') as example:
        soup = BeautifulSoup(example, 'html.parser')
    
    #page = requests.get(url)
    #soup = BeautifulSoup(page.text, 'html.parser')

    two_tables = soup.find('td', 'sites-layout-tile')
    try:
        routers, usb_typec = two_tables.find_all('tbody')
    except:
        return False

    routers_head = parse_header(routers.tr.find_all('td'))
    for router in routers.find_all('tr')[1:]:
        for _r in router:
            pass

    #with open(file, 'w') as f:
        #pass
        #json.dump(tickets, f)
        #return True

if __name__ == '__main__':
    pass

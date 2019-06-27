import json
import re

import requests
from bs4 import BeautifulSoup


url = (
    'https://www.chromium.org'
    '/chromium-os/developer-information-for-chrome-os-devices'
    )

files = [
    'boardnamedevices.json',
    'boardnamedevices-1.json',
    'boardnamedevices-2.json'
    ]

model = 'Model'
bname = 'Board name(s)'

to_remove = re.compile('^(x86-|_he)')

def sanitize(word):
    """Sanitizes a `word` to remove spaces including `\xa0`.

    Args:
        word: the word to sanitize

    Returns:
        str: the word, without the unnecessary stuff

    """
    return word.get_text(strip=True).replace('\xa0', ' ')


def simplify_board_name(board_name):
    """Removes the following from board names:
    - `x86-`, e.g. `x86-mario`
    - `_he`, e.g. `x86-alex_he`
    - `&` - e.g. `falco & falco_II`

    Args:
        board_name: the board name to simplify

    Returns:
        str: a simplified board name

    """
    if '&' in board_name:
        try:
            # always try to extract the first of two
            board_name = board_name.split('&')[0].strip()
        except Exception as e:
            print(e)
            pass
    return to_remove.sub('', board_name.lower())


def simplify_underscores(board_name):
    """Simplifies to use a common name `x` given a name in format `x_y`,
    discarding `_y`.

    Used for `boardnamedevices-2.json`.

    Args:
        board_name: the board name to simplify again

    Returns:
        str: a simplified board name

    """
    board_name = simplify_board_name(board_name)
    if '_' in board_name:
        try:
            # always try to extract the first of two
            board_name = board_name.split('_')[0].strip()
        except Exception as e:
            print(e)
            pass
    return to_remove.sub('', board_name.lower())


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
    idx[bname] = in_text.index(bname)
    return idx


def iterate_table(table, header = None):
    """Iterates through a `table` to retrieve `Model` and `Board name(s)`.

    Args:
        table: the table to parse
        header (optional): the bs4 header to use; defaults to None

    Returns:
        dict: of dicts with keys as `Board name(s)` and values as `Model`

    """
    jsons = {file: {} for file in files}
    if not header:
        header = table.tr.find_all('td')
    head = parse_header(header)
    for row in table.find_all('tr')[1:]:
        tds = row.find_all('td')
        _model = sanitize(tds[head[model]])

        _bname = simplify_board_name(sanitize(tds[head[bname]]))

        for _json in jsons:
            current = jsons[_json]
            if not _model and _json == files[0]:
                # for `boardnamedevices.json`, do not record blank names
                continue
            elif not _model:
                _model = "White Label"

            if _json == files[2]:
                _bname = simplify_underscores(_bname)

            if _bname in current:
                current[_bname] = '{}/{}'.format(
                    current[_bname],
                    _model
                    )
            else:
                current[_bname] = _model

    return jsons


def combine_dicts(dict_a, dict_b):
    """Combines two dicts of dicts into one. Specifically,
    combines two dicts with the keys = `files`.

    Args:
        dict_a (dict): dictionary a
        dict_b (dict): dictionary b

    Returns:
        dict[dict]: a combined dict

    """
    return {key: {**dict_a[key], **dict_b[key]} for key in dict_a}


def get_as_json():
    """Gets info as json."""
    jsons = {file: {} for file in files}

    # with open('example.html', 'r') as example:
    #     soup = BeautifulSoup(example, 'html.parser')
    
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    two_tables = soup.find('td', 'sites-layout-tile')
    try:
        routers, usb_typec = two_tables.find_all('tbody')
    except:
        return False

    main_header = (
        soup.find('table', 'goog-ws-list-header')
        .find('tr').find_all('th')
        )
    main_table = soup.find('table', 'sites-table').tbody

    for table in [routers, usb_typec]:
        jsons = combine_dicts(jsons, iterate_table(table))

    jsons = combine_dicts(jsons, iterate_table(main_table, main_header))

    for _json in jsons:
        with open(_json, 'w') as f:
            json.dump(jsons[_json], f, indent=4)
    return True

if __name__ == '__main__':
    get_as_json()

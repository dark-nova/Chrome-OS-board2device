import difflib
import json
import logging
import logging.handlers
import re
from collections import defaultdict
from typing import Dict, List

import pendulum
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet


LOGGER = logging.getLogger('cros-b2d')
LOGGER.setLevel(logging.DEBUG)

FH = logging.handlers.RotatingFileHandler(
    'cros-b2d.log',
    maxBytes=4096,
    backupCount=5,
    )
FH.setLevel(logging.DEBUG)

CH = logging.StreamHandler()
CH.setLevel(logging.INFO)

FH.setFormatter(
    logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    )
CH.setFormatter(
    logging.Formatter(
        '%(levelname)s - %(message)s'
        )
    )

LOGGER.addHandler(FH)
LOGGER.addHandler(CH)

URL = (
    'https://www.chromium.org'
    '/chromium-os/developer-information-for-chrome-os-devices'
    )

FILES = [
    'boardnamedevices',
    'boardnamedevices-1',
    'boardnamedevices-2'
    ]

MODEL = 'Model'
B_NAME = 'Board name(s)'

TO_REMOVE = re.compile('^(x86-|_he)')

JSON = Dict[str, List[str]] # {board name: [device 1, device 2]}
JSONS = Dict[str, JSON] # {json file: {board name: [...]}}


def sanitize(word: str) -> str:
    """Sanitizes a `word` to remove spaces including `\xa0`.

    Args:
        word: the word to sanitize

    Returns:
        str: the word, without the unnecessary stuff

    """
    return word.get_text(strip=True).replace('\xa0', ' ')


def simplify_board_name(board_name: str) ->  str:
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
        except AttributeError as e:
            LOGGER.info(e)
    return TO_REMOVE.sub('', board_name.lower())


def simplify_underscores(board_name: str) -> str:
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
        except AttributeError as e:
            LOGGER.info(e)
    return TO_REMOVE.sub('', board_name.lower())


def parse_header(header: ResultSet) -> Dict[str, int]:
    """Parses header to extract `Model` and `Board name(s)` positions.

    Args:
        header (ResultSet): the table header with at least 'Model' and
            'Board name(s)' columns

    Returns:
        dict: 0-based indices of the columns we want

    """
    idx = {}
    in_text = [td.get_text(strip=True) for td in header]
    idx[MODEL] = in_text.index(MODEL)
    idx[B_NAME] = in_text.index(B_NAME)
    return idx


def iterate_table(table: Tag, header: ResultSet = None) -> JSON:
    """Iterates through a `table` to retrieve `Model` and `Board name(s)`.

    Args:
        table (Tag): the table to parse
        header (ResultSet, optional): the bs4 header to use;
            defaults to None

    Returns:
        dict: of dicts with keys as `Board name(s)` and values as `Model`

    """
    jsons = {file: defaultdict(list) for file in FILES}
    if not header:
        header = table.tr.find_all('td')
    head = parse_header(header)
    for row in table.find_all('tr')[1:]:
        tds = row.find_all('td')
        model = sanitize(tds[head[MODEL]])

        board_name = simplify_board_name(sanitize(tds[head[B_NAME]]))

        for _json in jsons:
            current = jsons[_json]
            if not model and _json == FILES[0]:
                # for `boardnamedevices.json`, do not record blank names
                continue
            elif not model:
                model = "White Label"

            if _json == FILES[2]:
                board_name = simplify_underscores(board_name)

            current[board_name].append(model)

    return jsons


def combine_dicts(dict_a: JSONS, dict_b: JSONS) -> JSONS:
    """Combines two dicts of dicts into one. Specifically,
    combines two dicts with the keys = `FILES`. This is preferred
    over `dict.update`, because `dict.update` also overwrites
    existing information if keys collide.

    Args:
        dict_a (dict): dictionary a
        dict_b (dict): dictionary b

    Returns:
        dict: a combined dict

    """
    return {key: {**dict_a[key], **dict_b[key]} for key in dict_a}


def flatten_models(dicts: JSON) -> Dict[str, Dict[str, str]]:
    """Flattens models from `list` to `str`.

    If multiple models are found on a given board, delimit
    the results with '/', slash.

    Args:
        dicts (dict): a dictionary of 3 defaultdicts, with
            the 'default' being `list`

    Returns:
        dict: flattened

    """
    return {
        file: {
            board_name: ' | '.join(models)
            for board_name, models
            in contents.items()
            }
        for file, contents
        in dicts.items()
        }


def get_as_json() -> None:
    """Gets info as json."""
    jsons = {file: {} for file in FILES}

    # with open('example.html', 'r') as example:
    #     soup = BeautifulSoup(example, 'html.parser')
    
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')

    two_tables = soup.find('td', 'sites-layout-tile')
    try:
        routers, usb_typec = two_tables.find_all('tbody')
    except ValueError as e:
        LOGGER.error(e)
        return

    main_header = (
        soup.find('table', 'goog-ws-list-header')
        .find('tr').find_all('th')
        )
    main_table = soup.find('table', 'sites-table').tbody

    for table in [routers, usb_typec]:
        jsons = combine_dicts(jsons, iterate_table(table))

    jsons = combine_dicts(jsons, iterate_table(main_table, main_header))

    jsons = flatten_models(jsons)

    for _json in jsons:
        file = f'{_json}.json'
        with open(file, 'r') as f:
            old = json.load(f)
            if jsons[_json] == old:
                continue

        with open(file, 'w') as f:
            diff_file = f'{_json}.diff'
            dump = json.dumps(jsons[_json], indent=4)
            diff = [pendulum.today().strftime('%Y-%m-%d')]
            diff.append('===')
            diff.extend(
                [
                    d
                    for d
                    in difflib.ndiff(
                        json.dumps(old, indent=4).splitlines(),
                        dump.splitlines()
                        )
                    if d.startswith('+') or d.startswith('-')
                    ]
                )
            with open(diff_file, 'r') as g:
                old_diff = '\n\n' + g.read()
            with open(diff_file, 'w') as g:
                g.write('\n'.join(diff))
            with open(diff_file, 'a') as g:
                g.write(old_diff)
            f.write(dump)
  
    return


if __name__ == '__main__':
    get_as_json()

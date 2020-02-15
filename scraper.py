import difflib
import json
import re
from collections import defaultdict
from typing import Dict, List

import pendulum
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet

from config import LOGGER, MODEL_CHANGES


URL = (
    'https://www.chromium.org'
    '/chromium-os/developer-information-for-chrome-os-devices'
    )

FILES = [
    'boardnamedevices',
    'boardnamedevices-1',
    'boardnamedevices-2',
    ]

COL_MODEL = 'Model'
COL_BNAME = 'Board name(s)'

WL = 'WHITE_LABEL'

TO_REMOVE = re.compile('(x86-|_he)')

# Type-hints
JSON = Dict[str, List[str]] # {board name: [device 1, device 2]}
JSONS = Dict[str, JSON] # {json file: {board name: [...]}}


def sanitize(word: str) -> str:
    """Sanitizes a `word` to remove spaces including `\xa0`.

    Args:
        word (str): the word to sanitize

    Returns:
        str: the word, without the unnecessary stuff

    """
    return word.get_text(strip=True).replace('\xa0', ' ')


def simplify_board_name(board_name: str) ->  str:
    """Removes the following from board names:
    - `x86-`, e.g. `x86-mario`
    - `_he`, e.g. `x86-alex_he`
    - `&` - e.g. `falco & falco_II`
    - ',' - e.g. `hoho, but substitute a dp to vga chip` (why)

    Args:
        board_name: the board name to simplify

    Returns:
        str: a simplified board name

    """
    if '&' in board_name:
        # Always try to extract the first of two. For the time being,
        # only legacy devices have this format and the second element
        # is always the 'II' one.
        board_name = board_name.split('&')[0].strip()
    if ',' in board_name:
        # hohoho
        board_name = board_name.split(',')[0].strip()

    return TO_REMOVE.sub('', board_name.lower())


def simplify_underscores(board_name: str) -> str:
    """Simplifies to use a common name `x` given a name in the format
    `x_y`, discarding `_y` in the process.

    Used for `boardnamedevices-2.json`.

    Args:
        board_name (str): the board name to simplify again

    Returns:
        str: a simplified board name

    """
    if '_' in board_name:
        # Always try to extract the first of two, because the `x`
        # in the format `x_y` is the significant part of the name.
        board_name = board_name.split('_')[0].strip()

    return board_name


def parse_header(header: ResultSet) -> Dict[str, int]:
    """Parses header to extract `Model` and `Board name(s)` positions.

    Args:
        header (ResultSet): the table header with at least 'Model' and
            'Board name(s)' columns

    Returns:
        Dict[str, int]: 0-based indices of the columns we want

    """
    idx = {}
    in_text = [td.get_text(strip=True) for td in header]
    idx[COL_MODEL] = in_text.index(COL_MODEL)
    idx[COL_BNAME] = in_text.index(COL_BNAME)
    return idx


def iterate_table(table: Tag, header: ResultSet = None) -> JSONS:
    """Iterates through a `table` to retrieve `Model` and
    `Board name(s)`, creating three distinct JSONs.

    Args:
        table (Tag): the table to parse
        header (ResultSet, optional): the bs4 header to use;
            defaults to None

    Returns:
        JSONS: each JSON with `Board name(s)` as the keys and
            `Model` as the values

    """
    jsons = {file: defaultdict(list) for file in FILES}
    white_label = {file: defaultdict(int) for file in FILES}

    if not header:
        header = table.tr.find_all('td')

    head = parse_header(header)

    for row in table.find_all('tr')[1:]:
        tds = row.find_all('td')
        model = sanitize(tds[head[COL_MODEL]])

        board_name = simplify_board_name(sanitize(tds[head[COL_BNAME]]))

        # Fix errata in model names by comparing with the change list.
        if model in MODEL_CHANGES:
            model = MODEL_CHANGES[model]

        for file, contents in jsons.items():
            if file == FILES[2]:
                board_name = simplify_underscores(board_name)

            if not model and file == FILES[0]:
                # For `boardnamedevices.json`, do not record blank names
                continue
            elif model:
                contents[board_name].append(model)
            else:
                # This is a dummy value to remove later. This is to
                # preserve device order as seen on the source page.
                if WL not in contents[board_name]:
                    contents[board_name].append(WL)
                white_label[file][board_name] += 1

    for file, contents in jsons.items():
        for board_name, content in contents.items():
            content.sort()
            if board_name in white_label[file]:
                content.remove(WL)
                content.append(f'White Label ({white_label[file][board_name]})')

    return jsons


def combine_dicts(dict_a: JSONS, dict_b: JSONS) -> JSONS:
    """Combines two dicts of dicts into one. Specifically,
    combines two dicts with the keys = `FILES`. This is preferred
    over `dict.update`, because `dict.update` also overwrites
    existing information if keys collide.

    Args:
        dict_a (JSONS): dictionary a
        dict_b (JSONS): dictionary b

    Returns:
        JSONS: a combined dict

    """
    return {key: {**dict_a[key], **dict_b[key]} for key in dict_a}


def flatten_models(dicts: JSON) -> Dict[str, Dict[str, str]]:
    """Flattens models from `list` to `str`.

    If multiple models are found on a given board, delimit
    the results with ' | ', a pipe with surrounding spaces.

    Args:
        dicts (JSON): a dictionary of 3 defaultdicts, with
            the 'default' being `list`

    Returns:
        Dict[str, Dict[str, str]]: flattened

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


def create_jsons() -> None:
    """Create all JSON files and diffs for easier consumption."""
    jsons = {file: {} for file in FILES}

    # with open('example.html', 'r') as example:
    #     soup = BeautifulSoup(example, 'html.parser')
    
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')

    two_tables = soup.find('td', class_='sites-layout-tile')
    try:
        routers, usb_typec = two_tables.find_all('tbody')
    except ValueError as e:
        LOGGER.error(e)
        return

    main_header = (
        soup.find('table', class_='goog-ws-list-header')
        .find('tr').find_all('th')
        )
    main_table = soup.find('table', class_='sites-table').tbody

    for table in [routers, usb_typec]:
        jsons = combine_dicts(jsons, iterate_table(table))

    jsons = flatten_models(
        combine_dicts(
            jsons, iterate_table(main_table, main_header)
            )
        )

    for file, contents in jsons.items():
        diff_file = f'{file}.diff'
        file = f'{file}.json'

        # If no changes were detected, don't bother with checking for
        # diffs or create the file.
        try:
            with open(file, 'r') as f:
                old = json.load(f)
            if contents == old:
                continue
        except json.decoder.JSONDecodeError:
            # Since the "old" file doesn't exist, just make it an empty
            # dict. Because the file doesn't exist, there will be
            # certainly a diff generated.
            old = {}

        with open(file, 'w') as f:
            dump = json.dumps(contents, indent=4)
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

            if old:
                with open(diff_file, 'r') as g:
                    old_diff = '\n\n' + g.read()
            else:
                old_diff = ''
            with open(diff_file, 'w') as g:
                g.write('\n'.join(diff))
            with open(diff_file, 'a') as g:
                g.write(old_diff)

            f.write(dump)
  
    return


if __name__ == '__main__':
    create_jsons()

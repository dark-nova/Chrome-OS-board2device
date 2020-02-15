# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.4.0] - 2020-02-15
### Added
- Added more model name corrections. See `MODEL_CHANGES` in [`config.py`](config.py) and the file itself, [`model_changes.json`](model_changes.json). I admit these changes are a little heavy-handed, but many of these models broke consistency entirely.

### Changed
- Rearranged diffs. Moved breaking diff changes from formatting into appropriate `.old`.
- Semanting versioning is now `x.y.z` for all changes and retroactively.
- `White Label (1)` in any JSON should now just be `White Label`

## [1.3.5] - 2020-02-13
### Added
- Added missing/incomplete documentation
- Added fallback for when the JSON files don't yet exist or are empty

### Changed
- `try`-`except` removed for `board_name.split`; because only the first element counts, you cannot get an exception for splitting a `str` and using element 0.
- `,` is now filtered for board names. This only applies to `hoho, but substitute a dp to vga chip` (seriously)
- Logging moved to separate [config](config.py) module
- "White Label" devices are now **counted** rather than dumped (and potentially duplicated) in the list
- Individual devices are now sorted alphabetically, with "White Label" and its count at the end
- "ASUS-Chromebook-Flip-C214" is now correctly labeled "ASUS Chromebook Flip C214"
- Similarly, "AcerChromebook 11 (CB311-8H & CB311-8HT)" is "Acer Chromebook 11 (CB311-8H & CB311-8HT)"

## [1.3.4] - 2020-02-06
### Changed
- Project renamed from `Chrome OS board2device` to `board2device for ChromeOS`
- Readme updated
- License year updated

## [1.3.3] - 2019-12-01
### Added
- Lots of code polish
    - logging
    - better type-hints

### Changed
- Delimiter for multiple boards is now `<space>|<space>`. This is because multiple entries have characters like `/` (the previous delimiter) or `,` or `&` (both also potential delimiters).
    - This means that all the existing diffs were moved to `file.diff.old`. I'm sure that changing the delimiter would have caused the diffs to balloon in size.
- Readme cleaned up

## [1.3.2] - 2019-09-01
### Added
- Now using `collections.defaultdict` to handle boardname:model concatenation better
- Consequently, added a new function `flatten_models` that changes `list` to `str` for each board name entry

## [1.3.1] - 2019-09-01
### Changed
- Improved [readme](README.md)
- Line spacing on diffs

## [1.3.0] - 2019-06-26
### Added
- Diff files added to show changes between versions, timestamped
    - [`boardnamedevices.diff`](boardnamedevices-1.diff)
    - [`boardnamedevices-1.diff`](boardnamedevices-1.diff)
    - [`boardnamedevices-2.diff`](boardnamedevices-2.diff)
- Retroactively add changelog
- Some examples given for [`README.md`](README.md) ([section](README.md#simplification-of-board-names))

### Changed
- Updated [`requirements.txt`](requirements.txt)

### Removed
- `jsonlines.sh` is no longer necessary; instead, `json.dumps` uses `indent=4` for the equivalent pretty-printing.

## [1.2.0] - 2019-06-11
### Changed
- Outputs to all three variants instead of selectively via commenting

## [1.1.0] - 2019-05-21
### Added
- [`boardnamedevices-1.json`](boardnamedevices-1.json) adds back white label devices that are otherwise pruned from the base file
- [`boardnamedevices-2.json`](boardnamedevices-2.json) splits board names like `x_y` to use `x` instead

## [1.0.0] - 2019-05-11
### Added
- Initial version

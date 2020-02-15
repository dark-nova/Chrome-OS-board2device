# board2device for *[ChromeOS][CROS]*

## Overview

This project scrapes data from the [Developer Information page][CROSDEV] for *[ChromeOS][CROS]* and exports to JSONs.

In each JSON, the keys are the board names. Under each key (board name), you will find all devices that belong.

## Simplification of Board Names

Some board names share some names in common, so the script makes an attempt to group the devices together, using the common name.

1. Any model listed with two boards will only use the first board listed.

- `alex`: `x86-alex & x86-alex_he`
- `falco`: `falco & falco_li`
- `zgb`: `x86-zgb & x86-zgb_he`

2. `x86-` and `_he` on applicable boards are stripped.

- `alex`: `x86-alex` (after step 1)
- `mario`: `x86-mario`
- `zgb`: `x86-zgb` (after step 1)

3. Any and all models that share a common board will be as one string, delimited by `<space>|<space>`. i.e. `"board name": "device 1 | device 2"`, etc. (The ellipsis in the example below refers to a truncation of the entry.)

- `"hana": "Lenovo 100e Chromebook 2nd Gen (MTK) | ... | Poin2 Chromebook 14"`

4. ([`boardnamedevices-2.json`](boardnamedevices-2.json)) Board names with a sub-board name are ignored.

- `auron`: `auron_paine`, `auron_yuna`
- `daisy`: `daisy`, `daisy_skate`, `daisy_spring`
- `nyan`: `nyan_big`, `nyan_blaze`, `nyan_kitty`
- `parrot`: `parrot`, `parrot_ivb`
- `peach`: `peach_pi`, `peach_pit`
- `veyron`: `veyron_fievel`, `veyron_jaq`, etc.

## Standardization of Model Names

Several model names will undergo some standardization from their original values. Because these model names had typoes or formatting inconsistencies, I corrected entries according to my format; these changes can be found in [`model_changes.json`](model_changes.json).

1. All `&` ampersands were changed to be commas.
2. All `/` slashes were changed to be commas, with the exception of:
    - *Acer Chromebook 13 / Spin 13*
    - *Lenovo Thinkpad 11e Chromebook / Lenovo Thinkpad Yoga 11e Chromebook*
3. `Asus` was capitalized to match the majority of ASUS's listings.
4. If the manufacturer was missing, it was added. e.g. `Pixelbook` became `Google Pixelbook`
5. Extraneous spaces and punctuation were truncated.
6. If the model has multiple IDs associated, enclose all IDs in parentheses. e.g. `Acer Chromebook 11 (C730, C730E, C735)`
7. In the case of chipset manufacturers listed, e.g. `(MTK)`, those were left untouched.
8. In the case of `Samsung Chromebook Plus (V2)`, the parentheses were stripped to match other models like `HP Chromebook 11 G1` and `Lenovo 500e Chromebook 2nd Gen`.

### General Format

- `Manufacturer Model ID` if only one ID is listed
- `Manufacturer Model (ID-1, ..., ID-n)` for multiple IDs

## Diffs

Every JSON has an accompanying `.diff`. These diffs are sorted by date in descending chronological order with newest changes first. A `-` on a line refers to the original line, while a `+` refers to either an addition or a modification of a `-` line.

You may have also noticed the `.diff.old` files. These were created when I introduced breaking format changes that would have polluted each diff.

## Usage

After installing [requirements](#requirements), run [`scraper.py`](scraper.py).

## [Requirements](requirements.txt)

This code is designed around the following:

- Python 3.6+
    - `bs4`, used for scraping
    - `requests`, used in conjunction with `bs4`
    - `pendulum`, used for date and time
    - other [requirements](requirements.txt)

## Files

- [`boardnamedevices.json`](boardnamedevices.json) - the base JSON
- [`boardnamedevices-1.json`](boardnamedevices-1.json) - the same, with empty model names replaced with "White Label"
- [`boardnamedevices-2.json`](boardnamedevices-2.json) - the same as the 1st variant, with board names with underscores replaced with the "common" name
- [`boardnamedevices.diff`](boardnamedevices.diff) - diff of base JSON
- [`boardnamedevices-1.diff`](boardnamedevices-1.diff) - diff of 1st variant
- [`boardnamedevices-2.diff`](boardnamedevices-2.diff) - diff of 2nd variant
- [`boardnamedevices.diff.old`](boardnamedevices.diff.old) - obsolete diff of base JSON
- [`boardnamedevices-1.diff.old`](boardnamedevices-1.diff.old) - obsolete diff of 1st variant
- [`boardnamedevices-2.diff.old`](boardnamedevices-2.diff.old) - obsolete diff of 2nd variant
- [`model_changes.json`](model_changes.json) - changes to model names

## Live Version

These files are generated/updated every day at midnight Pacific Time via `cron`.

- [`boardnamedevices.json`][json-0]
- [`boardnamedevices-1.json`][json-1]
- [`boardnamedevices-2.json`][json-2]
- [`boardnamedevices.diff`][diff-0]
- [`boardnamedevices-1.diff`][diff-1]
- [`boardnamedevices-2.diff`][diff-2]

## Disclaimer

This project is not affiliated with or endorsed by *[Google][GOOGLE]*, *[Chromium][CHROMIUM]*, or *[Google Chrome][GCHROME]*. See [`LICENSE`](LICENSE) for more detail.

#### For the [r/ChromeOS](https://www.reddit.com/r/chromeos) Discord.

[json-0]: https://dark-nova.me/chromeos/boardnamedevices.json
[json-1]: https://dark-nova.me/chromeos/boardnamedevices-1.json
[json-2]: https://dark-nova.me/chromeos/boardnamedevices-2.json
[diff-0]: https://dark-nova.me/chromeos/boardnamedevices.diff.txt
[diff-1]: https://dark-nova.me/chromeos/boardnamedevices-1.diff.txt
[diff-2]: https://dark-nova.me/chromeos/boardnamedevices-2.diff.txt
[CHROMIUM]: https://www.chromium.org/
[CROS]: https://www.google.com/chromebook/
[CROSDEV]: https://www.chromium.org/chromium-os/developer-information-for-chrome-os-devices
[GOOGLE]: https://www.google.com/
[GCHROME]: https://www.google.com/chrome/

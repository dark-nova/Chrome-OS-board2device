# board2device for *[ChromeOS][CROS]*

## Overview

This project scrapes data from the [Developer Information page][CROSDEV] for *[ChromeOS][CROS]* and exports to JSONs.

The keys are the board names; the values are all devices that fit under that umbrella.

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

3. Any and all models that share a common board will be as one string, delimited by `<space>|<space>`. (i.e. `"board name": "device 1 | device 2"`, etc.)

- `hana: Lenovo N23 Yoga Chromebook | Poin2 Chromebook 14 | Poin2 Chromebook 11C | Lenovo 300e Chromebook | Lenovo Chromebook C330 | Lenovo Chromebook S330`

4. ([`boardnamedevices-2.json`](boardnamedevices-2.json)) Board names with a sub-board name are ignored.

- `auron`: `auron_paine`, `auron_yuna`
- `daisy`: `daisy`, `daisy_skate`, `daisy_spring`
- `nyan`: `nyan_big`, `nyan_blaze`, `nyan_kitty`
- `parrot`: `parrot`, `parrot_ivb`
- `peach`: `peach_pi`, `peach_pit`
- `veyron`: `veyron_fievel`, `veyron_jaq`, `veyron_jerry`, `veyron_mickey`, `veyron_mighty`, `veyron_minnie`, `veyron_speedy`, `veyron_tiger`,

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
- [`boardnamedevices.diff`](boardnamedevices.diff) - diff of base JSON
- [`boardnamedevices-1.diff`](boardnamedevices-1.diff) - diff of 1st variant
- [`boardnamedevices-2.diff`](boardnamedevices-2.diff) - diff of 2nd variant

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

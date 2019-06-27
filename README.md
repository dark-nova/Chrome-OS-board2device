# Chrome OS board2device

## What this does
Scrapes data from this [source](https://www.chromium.org/chromium-os/developer-information-for-chrome-os-devices). Outputs to JSON to process.

The keys are the board names; the values are all devices that fit under that umbrella.

### For the sake of simplicity
- Any model listed with two boards will only use the first board listed.
    - `x86-alex`, `x86-alex_he` -> `alex`
    - `falco`, `falco_li` -> `falco`
    - `x86-zgb`, `x86-zgb_he` -> `zgb`
- `x86-` and `_he` on applicable boards are stripped.
    - `x86-alex`, `x86-alex_he` -> `alex`
    - `x86-mario` -> `mario`
    - `x86-zgb`, `x86-zgb_he` -> `zgb`
- Any and all models that share a common board will be as one string, delimited by a slash `/`.
    - `hana`: `Lenovo N23 Yoga Chromebook/Poin2 Chromebook 14/Poin2 Chromebook 11C/Lenovo 300e Chromebook/Lenovo Chromebook C330/Lenovo Chromebook S330`
- ([`boardnamedevices-2.json`](boardnamedevices-2.json) only) Board names with a sub-board name are ignored.
    - `auron_paine`, `auron_yuna` -> `auron`
    - `daisy`, `daisy_skate`, `daisy_spring` -> `daisy`
    - `nyan_big`, `nyan_blaze`, `nyan_kitty` -> `nyan`
    - `parrot`, `parrot_ivb` -> `parrot`
    - `peach_pi`, `peach_pit` -> `peach`
    - `veyron_fievel`, `veyron_jaq`, `veyron_jerry`, `veyron_mickey`, `veyron_mighty`, `veyron_minnie`, `veyron_speedy`, `veyron_tiger` -> `veyron`

## Files
- [`boardnamedevices.json`](boardnamedevices.json) - the base JSON
- [`boardnamedevices-1.json`](boardnamedevices-1.json) - the same with empty model names replaced with "White Label"
- [`boardnamedevices-2.json`](boardnamedevices-2.json) - the same with also board names with underscores replaced with the "common" name
- [`boardnamedevices.diff`](boardnamedevices.diff) - diff of base JSON
- [`boardnamedevices-1.diff`](boardnamedevices-1.diff) - diff of 1st variant
- [`boardnamedevices-2.diff`](boardnamedevices-2.diff) - diff of 2nd variant
- [`example.html`](example.html) - the example from which I tested against
- [`requirements.txt`](requirements.txt) - the dependencies used for this project
- [`scraper.py`](scraper.py) - the scraper itself
- [`LICENSE`](LICENSE) - MIT License
- [`CHANGELOG.md`](CHANGELOG.md)
- [`README.md`](README.md) - this file

#### For the [r/ChromeOS](https://www.reddit.com/r/chromeos) Discord.

# Chrome OS board2device

## What this does
Scrapes data from this [source](https://www.chromium.org/chromium-os/developer-information-for-chrome-os-devices). Outputs to [`boardnamedevices.json`](boardnamedevices.json).

The keys are the board names; the values are all devices that fit under that umbrella.

### For the sake of simplicity
- Any model listed with two boards will only use the first board listed.
- `x86-` and `_he` on some boards are stripped.
- Any model that shares a common board will be as one string, delimited by a slash `/`.

## Files
- [`boardnamedevices.json`](boardnamedevices.json) - the current JSON
- [`example.html`](example.html) - the example from which I tested against
- [`jsonlines.sh`](jsonlines.sh) - a very barbaric way of pretty-printing (permanently) the JSON
- [`requirements.txt`](requirements.txt) - the dependencies used for this project
- [`scraper.py`] - the scraper itself

#### For the [r/ChromeOS](https://www.reddit.com/r/chromeos) Discord.

# Chrome OS board2device

## What this does
Scrapes data from this [source](https://www.chromium.org/chromium-os/developer-information-for-chrome-os-devices). Outputs to JSON to process.

The keys are the board names; the values are all devices that fit under that umbrella.

### For the sake of simplicity
- Any model listed with two boards will only use the first board listed.
- `x86-` and `_he` on applicable boards are stripped.
- Any and all models that share a common board will be as one string, delimited by a slash `/`.

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
- [`CHANGELOG`](CHANGELOG)

#### For the [r/ChromeOS](https://www.reddit.com/r/chromeos) Discord.

# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.3] - 2019-06-26
### Added
- Diff files added to show changes between versions, timestamped
    - [`boardnamedevices.diff`](boardnamedevices-1.diff)
    - [`boardnamedevices-1.diff`](boardnamedevices-1.diff)
    - [`boardnamedevices-2.diff`](boardnamedevices-2.diff)
- Retroactively add changelog

### Changed
- Updated [`requirements.txt`](requirements.txt)

### Removed
- `jsonlines.sh` is no longer necessary; instead, `json.dumps` uses `indent=4` for the equivalent pretty-printing.

## [1.2] - 2019-06-11
### Changed
- Outputs to all three variants instead of selectively via commenting

## [1.1] - 2019-05-21
### Added
- [`boardnamedevices-1.json`](boardnamedevices-1.json) adds back white label devices that are otherwise pruned from the base file
- [`boardnamedevices-2.json`](boardnamedevices-2.json) splits board names like `x_y` to use `x` instead

## [1.0] - 2019-05-11
### Added
- Initial version

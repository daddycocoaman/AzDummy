# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.2] - 2021-02-04

### Fixed

- Switched to builtin `importlib.metadata` for --version

## [1.1.1] - 2020-12-21

### Fixed

- Escaped password field to prevent Rich render errors

## [1.1.0] - 2020-12-19

### Changed

- Changed gitignore to ignore `output_*.csv` for generated output files
- Changed import location in `gen` module
- Changed output colors to match blue/white color theme of AzDummy

### Added

- Added output to show group membership in terminal
- Added output CSV files for bulk group membership import in Azure Portal
- Added `azdummy.styles`
- Added CHANGELOG.md and backfilled information. Whoops.

## [1.0.2] - 2020-12-15

### Fixed

- Reverted default locale to EN from RU

## [1.0.1] - 2020-12-15

### Fixed

- Removed unnecessary print statements for console output

## [1.0.0] - 2020-12-15

### Added

- Initial release

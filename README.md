<div align="center">
    <img src="https://github.com/daddycocoaman/AzDummy/raw/main/docs/images/AzDummy.png" width="400px" height="400px"/>
</div>

<div align="center">
    <img src="https://img.shields.io/pypi/v/azdummy"/>
    <img src="https://img.shields.io/pypi/pyversions/azdummy"/>
    <img src="https://img.shields.io/pypi/l/azdummy"/>
    <a href="https://twitter.com/mcohmi"><img src="https://img.shields.io/twitter/follow/mcohmi.svg?style=plastic"/></a>
</div>

# AzDummy
A Python [Typer-based](https://github.com/tiangolo/typer) CLI tool to generate fake data for Azure AD. AzDummy also uses [Rich](https://github.com/willmcgugan/rich) for some dope console output.

## Installation

The recommended method of installation is with [pipx](https://github.com/pipxproject/pipx). 

```
pipx install azdummy
```

However, you can install the normal way from PyPi with `python3 -m pip install azdummy`.

## Usage

On first run, user will be prompted to create a config file. Location of this config file depends on OS. **Note: There are some environment variables included that are currently not used.**

- Windows: 
  - `C:\Users\<user>\AppData\Roaming\azdummy\settings.env`
- Linux/Mac OS: 
  - `~/.azdummy/settings.env`

Currently used variables:

- **AZD_LOCALE**: (str) Shortcode for supported locales
- **AZD_TENANT_FQDN**: (str) One of the domains in the tenant (Usually `<domain>.onmicrosoft.com` format)
- **AZD_NUM_USERS**: (int) Number of users to generate  
- **AZD_BLOCK_LOGIN**: (bool) Block generated users from logging in
- **AZD_GROUP_NAMES**: (list) List of groups to add users to

**NOTE: Due to restrictions on the userPrincipalName field, all names are generated in English. However, AzDummy supports other locale-specific data generation (such as addresses).**

**Supported Locales:**
- CZECH = "cs"
- DANISH = "da"
- GERMAN = "de"
- AUSTRIAN_GERMAN = "de-at"
- SWISS_GERMAN = "de-ch"
- GREEK = "el"
- ENGLISH = "en"
- AUSTRALIAN_ENGLISH = "en-au"
- CANADIAN_ENGLISH = "en-ca"
- BRITISH_ENGLISH = "en-gb"
- SPANISH = "es"
- MEXICAN_SPANISH = "es-mx"
- ESTONIAN = "et"
- FARSI = "fa"
- FINNISH = "fi"
- FRENCH = "fr"
- HUNGARIAN = "hu"
- ICELANDIC = "is"
- ITALIAN = "it"
- JAPANESE = "ja"
- KAZAKH = "kk"
- KOREAN = "ko"
- DUTCH = "nl"
- BELGIUM_DUTCH = "nl-be"
- NORWEGIAN = "no"
- POLISH = "pl"
- PORTUGUESE = "pt"
- BRAZILIAN_PORTUGUESE = "pt-br"
- RUSSIAN = "ru"
- SLOVAK = "sk"
- SWEDISH = "sv"
- TURKISH = "tr"
- UKRAINIAN = "uk"
- CHINESE = "zh"
## Commands

Commands are available [here](docs/commands.md). You can generally use `--help/-h` for any command or subcommand for more information. With default settings, the following command will generate 500 users for `azdummy.onmicrosoft.com` (non-existant tenant).

`azdummy gen users` 

## What do I do with the output?

The default output provides two files for user: `output_create.csv` and `output_create.csv`. These files can be used with the Bulk Create and Bulk Delete options in Azure Portal in the Azure AD Users menu. Additionally, one file is created for each defined group with the members of those groups. These files can be used with the Import Members and Remove Members options in Azure Portal in the Azure AD Group menu.

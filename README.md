# ics2mail

This short Python script reads an ical file and sends today's events to a given email address. Correctly supports
recurring and all-day events. Sends both html and plain text. Fully configurable by changing values in config.py

## Requirements

- Python 3.9+
    - virtualenv

## Installation

Setup the virtualenv:

```bash
virtualenv .env && source .env/bin/activate && pip install -r requirements.txt
``` 

Or, if you're brave, just run install the requirements into your base python install:

```bash
pip install -r requirements.txt
```

Copy `config.ini.dist` to `config.ini` (or whatever name you choose) and enter ics and mail parameters into config.ini.
This config file **must** contain a section named "Mail" with the settings from `config.ini.dist` filled out. The other
sections can have any name you want (Other than "Mail"), and those names will be shown in the generated emails.

## Usage

```bash
source .env/bin/activate && python ics2mail.py <config_file>
```
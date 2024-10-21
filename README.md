# ics2mail

This short Python script reads an ical file and sends today's events to a given email address. Correctly supports recurring and all-day events. Sends both html and plain text. Fully configurable by changing values in config.py

## Requirements

- Python 3.x
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

Copy config.ini.dist to config.ini and enter ics and mail parameters into config.ini.

## Usage

```bash
source .env/bin/activate && python ics2mail.py <config_file>
```
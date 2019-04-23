# ics2mail

This short Python script reads an ical file and sends today's events to a given email address. Correctly supports recurring and all-day events. Sends both html and plain text. Fully configurable by changing values in config.py

## Requirements

- Python 3.x
  - icalevents
  
## Installation

Setup the virtualenv:
```bash
virtualenv .env && source .env/bin/activate && pip install -r requirements.txt
``` 

Copy config.py.dist to config.py and enter ics and mail parameters into config.py.

## Usage

```bash
python ics2mail.py
```
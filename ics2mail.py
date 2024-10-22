#! python3
import argparse
import configparser
import smtplib
import sys
import urllib.request
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import icalendar
import jinja2
import pytz
import recurring_ical_events


def event_value(event, key):
    try:
        return str(event[key])
    except KeyError:
        return ''


def main(argv):
    parser = argparse.ArgumentParser(prog='ics2mail',
                                     description='Consumes a number of given ics files and mails today\'s events to a given email address')
    parser.add_argument('config_file',
                        help='The path to a .ini file to read. See the provided config.ini.dist to get started.')
    parser.add_argument("-d", "--date", help='An optional date to check, in the format YYYY-MM-DD. Defaults to today.')
    args = parser.parse_args(argv)

    # Calculate today and tomorrow
    tz = pytz.timezone('US/Central')
    if args.date:
        today = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        now = datetime.now(tz)
        today = tz.localize(datetime(year=now.year, month=now.month, day=now.day))

    # Fetch the events
    should_send_mail = False

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("templates"),
        autoescape=jinja2.select_autoescape()
    )

    config = configparser.ConfigParser()
    config.read(args.config_file)
    mail_section = 'Mail'
    if not config.has_section(mail_section):
        sys.exit("No 'Mail' section found in "+args.config_file)

    parsed_calendars = {}
    for calendar in config.sections():
        if calendar != mail_section:
            print("Fetching events from '{:}'...".format(calendar))

            f = urllib.request.urlopen(config.get(calendar, 'url'))
            ical_string = f.read()
            ical = icalendar.Calendar.from_ical(ical_string)
            events = recurring_ical_events.of(ical).at((today.year, today.month, today.day))

            if len(events) > 0:
                should_send_mail = True

            parsed_events = []
            for event in events:
                parsed_events.append({
                    "all_day": event['X-MICROSOFT-CDO-ALLDAYEVENT'].to_ical() == b'TRUE',
                    "summary": event_value(event, 'summary'),
                    "location": event_value(event, 'location'),
                    "description": event_value(event, 'description'),
                    "start": event.start,
                    "end": event.end
                })
            parsed_calendars[calendar] = parsed_events

    # Send the email
    if should_send_mail:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '{:s} - {:%A, %B %d, %Y}'.format(config.get(mail_section, 'mail_subject'),
                                                          today)
        msg['From'] = config.get(mail_section, 'mail_from')
        msg['To'] = config.get(mail_section, 'mail_to')

        text_template = env.get_template('main.txt.jinja2')
        html_template = env.get_template('main.html.jinja2')

        text_body = text_template.render(calendars=parsed_calendars)
        html_body = html_template.render(calendars=parsed_calendars)

        part1 = MIMEText(text_body, 'plain')
        part2 = MIMEText(html_body, 'html')
        msg.attach(part1)
        msg.attach(part2)
        server = smtplib.SMTP(host=config.get(mail_section, 'smtp_server'),
                              port=config.get(mail_section, 'smtp_port', fallback=25))
        server.sendmail(config.get(mail_section, 'mail_from'),
                        config.get(mail_section, 'mail_to'), msg.as_string())
        server.quit()


if __name__ == '__main__':
    main(sys.argv[1:])

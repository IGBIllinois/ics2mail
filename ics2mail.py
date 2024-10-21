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
import pytz
import recurring_ical_events

import templates


def event_value(event, key):
    return str(event[key])


def main(argv):
    parser = argparse.ArgumentParser(prog='ics2mail', description='Consumes a number of given ics files and mails today\'s events to a given email address')
    parser.add_argument('config_file', help='The path to a .ini file to read. See the provided config.ini.dist to get started.')
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

    text_body = ""
    html_body = ""

    config = configparser.ConfigParser(allow_unnamed_section=True)
    config.read(args.config_file)

    for calendar in config.sections():
        if calendar != configparser.UNNAMED_SECTION:
            print("Fetching events from '{:}'...".format(calendar))

            f = urllib.request.urlopen(config.get(calendar, 'url'))
            ical_string = f.read()
            ical = icalendar.Calendar.from_ical(ical_string)
            events = recurring_ical_events.of(ical).at((today.year, today.month, today.day))

            if len(events) > 0:
                should_send_mail = True

            text_body += templates.header_text_template.format(calendar)
            html_body += templates.header_html_template.format(calendar)
            for event in events:
                if event['X-MICROSOFT-CDO-ALLDAYEVENT'].to_ical() == b'TRUE':
                    text_body += templates.all_day_text_template.format(event_value(event, 'summary'),
                                                                        event_value(event, 'location'),
                                                                        event_value(event, 'description'))
                    html_body += templates.all_day_html_template.format(event_value(event, 'summary'),
                                                                        event_value(event, 'location'),
                                                                        event_value(event, 'description'))
                else:
                    text_body += templates.event_text_template.format(event_value(event, 'summary'), event.start,
                                                                      event.end, event_value(event, 'location'),
                                                                      event_value(event, 'description'))
                    html_body += templates.event_html_template.format(event_value(event, 'summary'), event.start,
                                                                      event.end, event_value(event, 'location'),
                                                                      event_value(event, 'description'))
            if len(calendar) == 0:
                text_body += templates.none_text_template
                html_body += templates.none_html_template

    # Send the email
    if should_send_mail:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '{:s} - {:%A, %B %d, %Y}'.format(config.get(configparser.UNNAMED_SECTION, 'mail_subject'),
                                                          today)
        msg['From'] = config.get(configparser.UNNAMED_SECTION, 'mail_from')
        msg['To'] = config.get(configparser.UNNAMED_SECTION, 'mail_to')

        text_body = templates.text_template.format(text_body)
        html_body = templates.html_template.format(html_body)

        part1 = MIMEText(text_body, 'plain')
        part2 = MIMEText(html_body, 'html')
        msg.attach(part1)
        msg.attach(part2)
        server = smtplib.SMTP(host=config.get(configparser.UNNAMED_SECTION, 'smtp_server'),
                              port=config.get(configparser.UNNAMED_SECTION, 'smtp_port', fallback=25))
        server.sendmail(config.get(configparser.UNNAMED_SECTION, 'mail_from'),
                        config.get(configparser.UNNAMED_SECTION, 'mail_to'), msg.as_string())
        server.quit()


if __name__ == '__main__':
    main(sys.argv[1:])

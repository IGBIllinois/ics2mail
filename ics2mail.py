#! python
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from icalevents.icalevents import events
import pytz
import config

# Calculate today and tomorrow
tz = pytz.timezone('US/Central')
now = datetime.now(tz)
today = tz.localize(datetime(year=now.year, month=now.month, day=now.day))
tomorrow = today + timedelta(days=1)

# Fetch the events
calendar_events = []
events_to_print = False
for calendar in config.calendars:
    print("Fetching events from '{:}'...".format(calendar['title']))
    tmp_events = events(url=calendar['url'], start=today, end=tomorrow, no_recurrence='no_recurrence' in calendar and calendar['no_recurrence'])
    calendar_events.append(tmp_events)
    if len(tmp_events) > 0:
        events_to_print = True

# Send the email
if events_to_print:
    msg = MIMEMultipart('alternative')
    msg['Subject'] = '{:s} - {:%A, %B %d, %Y}'.format(config.mail_subject, today)
    msg['From'] = config.mail_from
    msg['To'] = config.mail_to
    text_body = ""
    html_body = ""
    for i, calendar in enumerate(calendar_events):
        text_body += config.header_text_template.format(config.calendars[i]['title'])
        html_body += config.header_html_template.format(config.calendars[i]['title'])
        for event in calendar:
            if event.all_day:
                text_body += config.all_day_text_template.format(event.summary, event.location, event.description)
                html_body += config.all_day_html_template.format(event.summary, event.location, event.description)
            else:
                text_body += config.event_text_template.format(event.summary, event.start.astimezone(tz),
                                                               event.end.astimezone(tz), event.location, event.description)
                html_body += config.event_html_template.format(event.summary, event.start.astimezone(tz),
                                                               event.end.astimezone(tz), event.location, event.description)
        if len(calendar) == 0:
            text_body += config.none_text_template
            html_body += config.none_html_template
    text_body = config.text_template.format(text_body)
    html_body = config.html_template.format(html_body)

    part1 = MIMEText(text_body, 'plain')
    part2 = MIMEText(html_body, 'html')
    msg.attach(part1)
    msg.attach(part2)
    server = smtplib.SMTP(host=config.smtp_server)
    server.sendmail(config.mail_from, config.mail_to, msg.as_string())
    server.quit()

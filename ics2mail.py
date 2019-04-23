#! python
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from icalevents.icalevents import events
from pytz import timezone
import config

# Calculate today and tomorrow
now = datetime.datetime.now()
tz = timezone('US/Central')
today = datetime.datetime(
    year=now.year,
    month=now.month,
    day=now.day,
    tzinfo=tz
)
tomorrow = today + datetime.timedelta(days=1)

# Fetch the events
events = events(url=config.cal_url, start=today, end=tomorrow)

# Send the email
if len(events) > 0:
    msg = MIMEMultipart('alternative')
    msg['Subject'] = '{:s} - {:%A, %B %d, %Y}'.format(config.mail_subject, today)
    msg['From'] = config.mail_from
    msg['To'] = config.mail_to
    text_body = ""
    html_body = ""
    for event in events:
        if event.all_day:
            text_body += config.all_day_text_template.format(event.summary, event.location, event.description)
            html_body += config.all_day_html_template.format(event.summary, event.location, event.description)
        else:
            text_body += config.event_text_template.format(event.summary, event.start.astimezone(tz),
                                                           event.end.astimezone(tz), event.location, event.description)
            html_body += config.event_html_template.format(event.summary, event.start.astimezone(tz),
                                                           event.end.astimezone(tz),
                                                           event.location, event.description)
    text_body = config.text_template.format(text_body)
    html_body = config.html_template.format(html_body)
    part1 = MIMEText(text_body, 'plain')
    part2 = MIMEText(html_body, 'html')
    msg.attach(part1)
    msg.attach(part2)
    server = smtplib.SMTP(host=config.smtp_server)
    server.sendmail(config.mail_from, config.mail_to, msg.as_string())
    server.quit()

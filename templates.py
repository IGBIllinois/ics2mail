#! python3
# todo update this nonsense with a jinja2 template
text_template = "{:s}"
html_template = """\
<html>
  <head>
    <style>
      table {{
        margin-bottom: 1.5rem;
      }}
      th {{
        padding-right: 1rem;
        text-align: left;
        vertical-align: top;
      }}
      td pre {{
        font-family: initial;
        white-space: pre-wrap;
        word-wrap: break-word;
      }}
    </style>
  </head>
  <body>
    {:s}
  </body>
</html>
"""

header_text_template = """\
{:s}:

"""
header_html_template = """\
<h4>{:s}<h4>
"""

event_text_template = """\
Event:     \t\t{0:s}
Start:     \t\t{1:%I:%M %p}
End:       \t\t{2:%I:%M %p}
Location:  \t{3:s}
Description:
{4:s}

"""
all_day_text_template = """\
Event:     \t\t{0:s}
All-day
Location:  \t{1:s}
Description:
{2:s}

"""
none_text_template = """\
No Events

"""

event_html_template = """\
<table>
  <tr>
    <th>Event</th><td>{:s}</td>
  </tr>
  <tr>
    <th>Start</th><td>{:%I:%M %p}</td>
  </tr>
  <tr>
    <th>End</th><td>{:%I:%M %p}</td>
  </tr>
  <tr>
    <th>Location</th><td>{:s}</td>
  </tr>
  <tr>
    <th>Description</th><td><pre>{:s}</pre></td>
  </tr>
</table>
"""
all_day_html_template = """\
<table>
  <tr>
    <th>Event</th><td>{:s}</th>
  </tr>
  <tr>
    <th colspan="2">All day</th>
  </tr>
  <tr>
    <th>Location</td><td>{:s}</th>
  </tr>
  <tr>
    <th>Description</td><td>{:s}</th>
  </tr>
</table>
"""

none_html_template = """\
<table>
    <tr>
        <td>No Events</td>
    </tr>
</table>

"""

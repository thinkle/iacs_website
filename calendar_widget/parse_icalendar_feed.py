from icalendar import Calendar, Event
import datetime
from dateutil import tz
import urllib

fi = file('basic.ics','rb')
str = fi.read(); fi.close()
c = Calendar.from_ical(str)

def remove_leading_zero (s):
    if s[0]=='0': return s[1:]
    else: return s

def get_events_near_today (c, before=1, after=5):
    keepers = []
    for event in c.walk():
        for prop in ['dtstart','dtend']:
            if event.get(prop):
                event_date = event.get(prop).dt
                if hasattr(event_date,'date'):
                    event_date = event_date.date()
                try:
                    distance = datetime.date.today() - event_date
                except:
                    print 'Problem with:',event_date,type(event_date)
                    raise
                days = distance.days
                if (-(after) < days < before):
                    if event not in keepers:
                        keepers.append(event)
    return keepers

def get_events_near_today_from_uri (uri, color='red',**kwargs):
    fi = urllib.urlopen(uri)
    c = Calendar.from_ical(fi.read())
    events = get_events_near_today(c,**kwargs)
    for e in events:
        e.color = color
    return events

def format_calendar (events):
    # Sort events...
    events.sort(key=lambda x: x.get('dtstart').dt.timetuple())
    events_by_days = {}
    for e in events:
        start = e.get('dtstart').dt
        end = e.get('dtend').dt
        if hasattr(start,'date'):
            start = start.astimezone(tz.tzlocal())
            start_date = start.date()
        else:
            start_date = start
        if hasattr(end,'date'):
            end = end.astimezone(tz.tzlocal())
            end_date = end.date()
        else:
            end_date = end
        e.start = start; e.start_date = start_date; e.end = end; e.end_date = end_date # shorthand...
        if not events_by_days.has_key(start_date):
                events_by_days[start_date] = []
        events_by_days[start_date].append(e)
    html = ''
    days = events_by_days.keys()
    days.sort()
    for d in days:
        html += '<div class="day_container"><h3 class="day">' + d.strftime('%B %d') + '</h3>\n'
        html += '<table class="schedule">'
        alternator = True
        for e in events_by_days[d]:
            klass = (alternator and 'event1') or 'event2'
            alternator = not alternator
            html += '<tr class="%s" style="color:'%klass + e.color + '">'
            html += '<td class="time">' # Start time
            if hasattr(e.get('dtstart').dt,'date'): # If it's a time...
                html += remove_leading_zero(e.start.astimezone(tz.tzlocal()).strftime('%I:%M%p'))
                if e.end != e.start:
                    # If differ end-time than start time
                    html += '-' + remove_leading_zero(e.end.astimezone(tz.tzlocal()).strftime('%I:%M%p'))
            elif e.start_date != e.end_date:
                # If the dates differ, we'll specify in the time section, semi-awkwardly...
                print 'Interesting -- more than one day for this event'
                print e.start_date,e.end_date,e.get('summary')
                if (e.end_date - e.start_date).days == 1:
                    print 'Ignoring -- only 1 day difference; appears to be an all-day, timeless event'
                else:
                    html += remove_leading_zero(e.start_date.strftime('%m/%d')) + '-' + remove_leading_zero(e.end_date.strftime('%m/%d'))
            html += '</td>' # End time
            html += '<td class="summary">' + e.get('summary') + '</td>'
            html += '</tr>\n' # End row
        html += '</table>\n</div>\n'
    return html

 
events1 = get_events_near_today_from_uri('http://www.google.com/calendar/ical/innovationcharter.org_4f5nt4qijeoblj11aj2q7hibdc%40group.calendar.google.com/public/basic.ics')
events2 = get_events_near_today_from_uri('http://www.google.com/calendar/ical/innovationcharter.org_f18ij5fhojmf19fnjtlkcs0gvo%40group.calendar.google.com/public/basic.ics',color='green')


css = '''<style type="text/css">
.schedule {font-size:small;font-family:arial}
.time {width:8em}
.day_container {margin-top:0px;margin-bottom:.5em;font-weight:bold}
.event2 {background-color: #dcd}
.event1 {background-color: #fef}
.day {margin-top:0px;margin-bottom:5px;font-size:small}
</style>
'''
head = '<html><head>'+css+'</head><body>'
foot = '</body></html>'

ofi = file('/tmp/test.html','w')
ofi.write(head)
ofi.write( format_calendar(events1+events2))
ofi.write(foot)
ofi.close()

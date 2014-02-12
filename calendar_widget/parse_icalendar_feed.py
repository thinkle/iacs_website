from icalendar import Calendar, Event
import datetime
from dateutil import tz

fi = file('basic.ics','rb')
str = fi.read(); fi.close()
c = Calendar.from_ical(str)

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
        html += '<table>'
        for e in events_by_days[d]:
            html += '<tr>'
            html += '<td class="time">' # Start time
            if hasattr(e.get('dtstart').dt,'date'): # If it's a time...
                html += e.start.astimezone(tz.tzlocal()).strftime('%I:%M%p')
                if e.end != e.start:
                    # If differ end-time than start time
                    html += '-' + e.end.astimezone(tz.tzlocal()).strftime('%I:%M%p')
            elif e.start_date != e.end_date:
                # If the dates differ, we'll specify in the time section, semi-awkwardly...
                print 'Interesting -- more than one day for this event'
                print e.start_date,e.end_date,e.get('summary')
                if (e.end_date - e.start_date).days == 1:
                    print 'Ignoring -- only 1 day difference; appears to be an all-day, timeless event'
                else:
                    html += e.start_date.strftime('%m/%d') + '-' + e.end_date.strftime('%m/%d')
            html += '</td>' # End time
            html += '<td class="summary">' + e.get('summary') + '</td>'
            html += '</tr>\n' # End row
            html += '</table>\n</div>\n'
    return html

 
        
    

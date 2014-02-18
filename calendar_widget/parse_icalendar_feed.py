from icalendar import Calendar, Event
import datetime
from dateutil import tz
import urllib

#fi = file('basic.ics','rb')
#str = fi.read(); fi.close()
#c = Calendar.from_ical(str)

def remove_leading_zero (s):
    if s[0]=='0': return s[1:]
    else: return s

def format_time_property (p):
    dt = p.dt
    if hasattr(dt,'date'): # If it's a time...
        return dt.astimezone(tz.tzlocal()).strftime('%A %B %d, %I:%M%p')
    else:
        return dt.strftime('%A %B %d')
        
def get_events_near_today (c, before=5, after=21):
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

def format_calendar (events, hide_before=True, hide_after_rows=10):
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
    row_count = 0; past_max_rows = False; end_hide_before = False
    if hide_before == True:
            html += '<a class="more_button"x href="#" onclick="javascript:toggle(\'before\')">Earlier...</a>'
            html += '<div class="hidden" id="before">'
    for d in days:
        if (hide_before and not end_hide_before and d >= d.today()):
            html += '</div>' # End hidden container...
            row_count = 0
            end_hide_before = True
        if not past_max_rows and (row_count > hide_after_rows):
            html+= '''<div class="hidden" id="hidden_after">'''
            print 'Passed max rows!'
            past_max_rows = True
        html += '<div class="day_container"><h3 class="day">' + d.strftime('%B %d') + '</h3>\n'
        row_count += 1
        html += '<table class="schedule">'
        alternator = True
        for e in events_by_days[d]:
            row_count += 1
            klass = (alternator and 'event1') or 'event2'
            alternator = not alternator
            html += '<tr class="%s">'%klass
            html += '<td class="time">' # Start time
            if hasattr(e.get('dtstart').dt,'date'): # If it's a time...
                html += remove_leading_zero(e.start.astimezone(tz.tzlocal()).strftime('%I:%M%p'))
                #if e.end != e.start:
                 #   # If differ end-time than start time
                 #   html += '-' + remove_leading_zero(e.end.astimezone(tz.tzlocal()).strftime('%I:%M%p'))
            elif e.start_date != e.end_date:
                # If the dates differ, we'll specify in the time section, semi-awkwardly...
                print 'Interesting -- more than one day for this event'
                print e.start_date,e.end_date,e.get('summary')
                if (e.end_date - e.start_date).days == 1:
                    print 'Ignoring -- only 1 day difference; appears to be an all-day, timeless event'
                else:
                    html += remove_leading_zero(e.start_date.strftime('%m/%d')) + '-' + remove_leading_zero(e.end_date.strftime('%m/%d'))
            html += '</td>' # End time
            html += '<td class="summary" style="color:%s">'%e.color
            html += '<a style="text-decoration:none;color:%s" href="#" onclick="javascript:toggle(\'%s\')">'%(e.color,e.get('uid'))
            html += e.get('summary')
            html += '</a>'
            html += '<div class="hidden_box" id="' + e.get('uid') + '">'
            # Hidden material...
            html += '''
            <p class="start">Start: %(start)s</p>
            <p class="end">End: %(end)s</p>
            <p class="desc">Description: %(description)s</p>
            <p class="location">Location: %(location)s</p>
            <p class="created">Created: %(created)s</p>
            <p class="lastmod">Last Modified: %(lastmod)s</p>
            <p class="status">Status: %(status)s</p>
            '''%{
                'status':e.get('status'),
                'start':format_time_property(e.get('dtstart')),
                'end':format_time_property(e.get('dtend')),
                'created':format_time_property(e.get('created')),
                'lastmod':format_time_property(e.get('last-modified')),
                'description':''+e.get('description'),
                'location':''+e.get('location'),
                }
            html += '</div>' # End hidden material
            html += '</td>'
            html += '</tr>\n' # End row
        html += '</table>\n</div>\n'
    if past_max_rows:
        html+= '''</div>
        <a class="more_button" href="#" onclick="javascript:toggle('hidden_after')">More...</a>'''
    return html

def suck_file (fn):
    fi = file(fn,'r')
    ret = fi.read()
    fi.close()
    return ret

head = suck_file('html_head.html')
foot = suck_file('html_foot.html')

def write_events (fn, events):
    ofi = file(fn,'w')
    ofi.write(head)
    ofi.write( format_calendar(events))
    ofi.write(foot)
    ofi.close()
    
def write_feeds (fn, feeds_and_colors):
    events = []
    for f,color in feeds_and_colors:
        events = events + get_events_near_today_from_uri(f,color=color)
    write_events(fn,events)

if __name__ == '__main__':
    write_feeds('/tmp/test.html',
                [('http://www.google.com/calendar/ical/innovationcharter.org_4f5nt4qijeoblj11aj2q7hibdc%40group.calendar.google.com/public/basic.ics','red'),
                 ('http://www.google.com/calendar/ical/innovationcharter.org_f18ij5fhojmf19fnjtlkcs0gvo%40group.calendar.google.com/public/basic.ics','green'),
                 ]
                 )


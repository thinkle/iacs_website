from icalendar import Calendar, Event
import datetime
from dateutil import tz
import urllib
import gdoc_writer 
import tempfile


#fi = file('basic.ics','rb')
#str = fi.read(); fi.close()
#c = Calendar.from_ical(str)

def remove_leading_zero (s):
    if s[0]=='0': return s[1:]
    else: return s

def format_time_property (p, short=False):
    dt = p.dt
    if hasattr(dt,'date'): # If it's a time...
        if short:
            return dt.astimezone(tz.tzlocal()).strftime('%m/%d %I:%M%p')
        else:
            return dt.astimezone(tz.tzlocal()).strftime('%A, %B %d, %I:%M%p')
    else:
        if short:
            return dt.strftime('%m/%d')
        else:
            return dt.strftime('%A, %B %d')
        
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
    try:
        c = Calendar.from_ical(fi.read())
    except:
        print 'Error reading: ',uri
        raise
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
        today = start_date.today()
        if (end_date - start_date).days > 1 and end_date > today and start_date < today:
                if not events_by_days.has_key(today):
                        events_by_days[today] = []
                events_by_days[today].append(e)                      
    html = ''
    days = events_by_days.keys()
    days.sort()
    row_count = 0; past_max_rows = False; end_hide_before = False
    if hide_before == True:
            html += '<a class="more_button"x href="#_" onclick="javascript:toggle(\'before\')">Earlier...</a>'
            html += '<div class="hidden" id="before"> <!-- Before -->'
    for d in days:
        if ((hide_before and not end_hide_before) and d >= d.today()):
            html += '</div> <!-- End Before -->' # End hidden container...
            row_count = 0
            end_hide_before = True
        if end_hide_before and not past_max_rows and (row_count > hide_after_rows):
            html+= '''<div class="hidden" id="hidden_after"> <!-- Start after -->'''
            past_max_rows = True
        html += '<div class="day_container"><h3 class="day">' + d.strftime('%A, %B %d') + '</h3>\n'
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
                #print 'Interesting -- more than one day for this event'
                #print e.start_date,e.end_date,e.get('summary')
                if (e.end_date - e.start_date).days == 1:
                    if False: # Don't print debug statement - this is really common
                        print 'Ignoring -- only 1 day difference; appears to be an all-day, timeless event'
                else:
                    html += remove_leading_zero(e.start_date.strftime('%m/%d')) + '-' + remove_leading_zero(e.end_date.strftime('%m/%d'))
            html += '</td>' # End time
            html += '<td class="summary" style="color:%s">'%e.color
            html += '<a style="text-decoration:none;color:%s" href="#_" onclick="javascript:toggle(\'%s\')">'%(e.color,e.get('uid'))
            html += e.get('summary')
            html += '</a>'
            html += '<div class="hidden_box" id="' + e.get('uid') + '">'
            # Hidden material...
            html += '''
            <p class="start">Start: %(start)s</p>
            <p class="end">End: %(end)s</p>'''%{
                'start':format_time_property(e.get('dtstart')),
                'end':format_time_property(e.get('dtend')),
                }
            if e.get('description'):
                html += '<p class="desc">Description: %(description)s</p>'%{'description':''+e.get('description')}
            if e.get('location'):
                html += '<p class="location">Location: %(location)s</p>'%{'location':''+e.get('location')}
            html += '''
            <p class="created">Created: %(created)s</p>
            <p class="lastmod">Last Modified: %(lastmod)s</p>
            <p class="status">Status: %(status)s</p>
            '''%{
                'status':e.get('status'),
                'created':format_time_property(e.get('created'),True),
                'lastmod':format_time_property(e.get('last-modified'),True),
                }
            html += '</div>' # End hidden material
            html += '</td>'
            html += '</tr>\n' # End row
        html += '</table>\n</div>\n'
    if past_max_rows:
        html+= '''</div>
        <a class="more_button" href="#_" onclick="javascript:toggle('hidden_after')">More...</a>'''
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

def write_feeds_to_gdoc (gdoc_id, feeds_and_colors):
    tmpfile = tempfile.mktemp()
    write_feeds(tmpfile,feeds_and_colors)
    gdoc_writer.update_resource_from_file(gdoc_id,tmpfile)

def write_feeds_to_file (fname, feeds_and_colors):
    f = file(fname, 'w')
    write_feeds(fname,feeds_and_colors)
    f.close()
    
    
if __name__ == '__main__':
    write_feeds('/tmp/test.html',
                [('http://www.google.com/calendar/ical/innovationcharter.org_4f5nt4qijeoblj11aj2q7hibdc%40group.calendar.google.com/public/basic.ics',COLOR1),
                 #('http://www.google.com/calendar/ical/innovationcharter.org_f18ij5fhojmf19fnjtlkcs0gvo%40group.calendar.google.com/public/basic.ics',COLOR2),
                 ]
                 )


import parse_icalendar_feed

MAIN_COLOR = 'rgb(158,0,50)' # reddish
MS_SPORTS_COLOR = 'rgb(108,0,158)' # purple
HS_SPORTS_COLOR = 'rgb(0,158,29)' # green
COLOR4 = 'rgb(158,108,0)' # brown

ALL_SCHOOL_CALENDARS = [
    'http://www.google.com/calendar/ical/innovationcharter.org_4f5nt4qijeoblj11aj2q7hibdc%40group.calendar.google.com/public/basic.ics', # 'IACS All School Public Calendar'
    ]

MS_SPORTS_CALENDARS = [
    'http://www.google.com/calendar/ical/innovationcharter.org_08i6r2k9g43cjjdno7hi1msrkk%40group.calendar.google.com/public/basic.ics', # 'MS Dance'
    'http://www.google.com/calendar/ical/innovationcharter.org_oasth6j7iuneujrr52uh26q32o%40group.calendar.google.com/public/basic.ics', # 'MS Boys JV Basketball'
    'http://www.google.com/calendar/ical/innovationcharter.org_s0b7cmnnjaon878f91sdmjnfc8%40group.calendar.google.com/public/basic.ics', # 'MS Cheerleading'
    'http://www.google.com/calendar/ical/innovationcharter.org_r1l94j47sfooj5ekj9nberhkqg%40group.calendar.google.com/public/basic.ics', # 'MS Girls Varsity Basketball'
    'http://www.google.com/calendar/ical/innovationcharter.org_ljrcu8nca3eacpcmjr8nqo7c24%40group.calendar.google.com/public/basic.ics', # 'MS Girls JV Basketball'
    ]

HS_SPORTS_CALENDARS = [
    'http://www.google.com/calendar/ical/innovationcharter.org_q0rlftcbppcstvnv71i1fp0s2g%40group.calendar.google.com/public/basic.ics', # 'HS Girls Varsity Basketball'
    'http://www.google.com/calendar/ical/innovationcharter.org_6ddkakvq3b9khj62c4nrda1834%40group.calendar.google.com/public/basic.ics', # 'HS Girls JV Basketball'
    'http://www.google.com/calendar/ical/innovationcharter.org_hlv39ln746erhs8v1qrb9sfqe8%40group.calendar.google.com/public/basic.ics', # 'Boys Varsity Basketball'
    'http://www.google.com/calendar/ical/innovationcharter.org_71lk8jhipqffq1ngga2jlon6m0%40group.calendar.google.com/public/basic.ics', # 'HS Cheerleading'
    'http://www.google.com/calendar/ical/innovationcharter.org_vr6fspiu1in9sj3uio02c9hcd0%40group.calendar.google.com/public/basic.ics', # 'Indoor Track and Field'
    'http://www.google.com/calendar/ical/innovationcharter.org_p9tpifvtoaghvufdho81v642fk%40group.calendar.google.com/public/basic.ics', # 'HS Boys Varsity Basketball'
    'http://www.google.com/calendar/ical/innovationcharter.org_s6h841d8b6g3gkuiqtqievuvnc%40group.calendar.google.com/public/basic.ics', # 'HS Boys JV Basketball'
    ]

# For main page...
main_feeds = [(f,MAIN_COLOR) for f in ALL_SCHOOL_CALENDARS] + [(f,MS_SPORTS_COLOR) for f in MS_SPORTS_CALENDARS] + [(f,HS_SPORTS_COLOR) for f in HS_SPORTS_CALENDARS]
parse_icalendar_feed.write_feeds_to_gdoc(
    '0B-fhMzqaF6ywRFVjNVVDQlVPU1U',
    main_feeds)


import parse_icalendar_feed

COLOR1 = MAIN_COLOR = 'rgb(158,0,50)' # reddish
COLOR2 = MS_SPORTS_COLOR = 'rgb(108,0,158)' # purple
COLOR3 = HS_SPORTS_COLOR = 'rgb(0,158,29)' # green
COLOR4 = 'rgb(158,108,0)' # brown
#COLOR5 =

COLORS = [COLOR1,COLOR2,COLOR3,COLOR4]

ALL_SCHOOL_CALENDARS = [
    'http://www.google.com/calendar/ical/innovationcharter.org_4f5nt4qijeoblj11aj2q7hibdc%40group.calendar.google.com/public/basic.ics', # 'IACS All School Public Calendar'
    ]

MS_SPORTS_CALENDARS = [
    'http://www.google.com/calendar/ical/innovationcharter.org_08i6r2k9g43cjjdno7hi1msrkk%40group.calendar.google.com/public/basic.ics', # color=#4CB052, MS Dance
    'http://www.google.com/calendar/ical/innovationcharter.org_hlv39ln746erhs8v1qrb9sfqe8%40group.calendar.google.com/public/basic.ics', # color=#E67399, MS Boys Varsity Basketball
    'http://www.google.com/calendar/ical/innovationcharter.org_0m1l7efrle9k1f1fic2gfegbq4%40group.calendar.google.com/public/basic.ics', # color=#65AD89, MS Volleyball    
    'http://www.google.com/calendar/ical/innovationcharter.org_oasth6j7iuneujrr52uh26q32o%40group.calendar.google.com/public/basic.ics', # color=#59BFB3, MS Boys JV Basketball
    'http://www.google.com/calendar/ical/innovationcharter.org_s0b7cmnnjaon878f91sdmjnfc8%40group.calendar.google.com/public/basic.ics', # color=#B373B3, MS Cheerleading
    'http://www.google.com/calendar/ical/innovationcharter.org_r1l94j47sfooj5ekj9nberhkqg%40group.calendar.google.com/public/basic.ics', # color=#BFBF4D, MS Girls Varsity Basketball
    'http://www.google.com/calendar/ical/innovationcharter.org_ljrcu8nca3eacpcmjr8nqo7c24%40group.calendar.google.com/public/basic.ics', # color=#8CBF40, MS Girls JV Basketball
    'http://www.google.com/calendar/ical/innovationcharter.org_vr6fspiu1in9sj3uio02c9hcd0%40group.calendar.google.com/public/basic.ics', # color=#A7A77D, Indoor Track
    'http://www.google.com/calendar/ical/innovationcharter.org_j82ju4qm8h0f79qlskj4pqlfvk%40group.calendar.google.com/public/basic.ics', # color=#C4A883, MS Track &amp; Field
'http://www.google.com/calendar/ical/innovationcharter.org_6pj0mcu04f4bvvlvmh28n0unvs%40group.calendar.google.com/public/basic.ics', # color=#8C66D9, MS Softball
'http://www.google.com/calendar/ical/innovationcharter.org_56spadvgqpb9du9a8lq5eimugs%40group.calendar.google.com/public/basic.ics', # color=#E6804D, MS Girls Soccer
'http://www.google.com/calendar/ical/innovationcharter.org_br2jhttn8a8vh5shk1pn29h7qs%40group.calendar.google.com/public/basic.ics', # color=#E0C240, MS Cross Country
'http://www.google.com/calendar/ical/innovationcharter.org_4qn88fisi3sg6slkqhb5vasbn8%40group.calendar.google.com/public/basic.ics', # color=#D96666, MS Boys Soccer
'http://www.google.com/calendar/ical/innovationcharter.org_galk1b9qijtq06kdcuanj90aig%40group.calendar.google.com/public/basic.ics', # color=#668CD9, MS Baseball
    ]

HS_SPORTS_CALENDARS = [
    'http://www.google.com/calendar/ical/innovationcharter.org_l9c9t9ep2e9piaecf9p23qq33o%40group.calendar.google.com/public/basic.ics',
    # V Boys Soccer color=#668CD9
    'http://www.google.com/calendar/ical/innovationcharter.org_eu82h40tl4135js0ubvi11rci4%40group.calendar.google.com/public/basic.ics',
    #color=#D96666, V Girls Soccer
    'http://www.google.com/calendar/ical/innovationcharter.org_40ptgt6b4m9q7kl4dronrpq1rg%40group.calendar.google.com/public/basic.ics',
    #color=#E0C240, High &amp; Middle School Track - MEET Schedule
    'http://www.google.com/calendar/ical/innovationcharter.org_s6h841d8b6g3gkuiqtqievuvnc%40group.calendar.google.com/public/basic.ics',
    #color=#4CB052, HS Boys JV Basketball
    'http://www.google.com/calendar/ical/innovationcharter.org_p9tpifvtoaghvufdho81v642fk%40group.calendar.google.com/public/basic.ics',
    #color=#E6804D, HS Boys Varsity Basketball
    'http://www.google.com/calendar/ical/innovationcharter.org_71lk8jhipqffq1ngga2jlon6m0%40group.calendar.google.com/public/basic.ics',
    #color=#8C66D9, HS Cheerleading
    'http://www.google.com/calendar/ical/innovationcharter.org_6ddkakvq3b9khj62c4nrda1834%40group.calendar.google.com/public/basic.ics',
    #color=#C4A883, HS Girls JV Basketball
    'http://www.google.com/calendar/ical/innovationcharter.org_q0rlftcbppcstvnv71i1fp0s2g%40group.calendar.google.com/public/basic.ics',
    #color=#65AD89, HS Girls Varsity Basketball
    'http://www.google.com/calendar/ical/innovationcharter.org_vr6fspiu1in9sj3uio02c9hcd0%40group.calendar.google.com/public/basic.ics',
    #color=#85AAA5, Indoor Track
    ]

# For main page...
main_feeds = [(f,MAIN_COLOR) for f in ALL_SCHOOL_CALENDARS] + [(f,MS_SPORTS_COLOR) for f in MS_SPORTS_CALENDARS]
# Add HS manually to prevent repeats...
for feed in HS_SPORTS_CALENDARS:
    if feed not in MS_SPORTS_CALENDARS:
        main_feeds.append((f,HS_SPORTS_COLOR))

parse_icalendar_feed.write_feeds_to_gdoc(
    '0B-fhMzqaF6ywRFVjNVVDQlVPU1U',
    main_feeds)

CUR_COL = -1
def alternate_color ():
    global CUR_COL
    CUR_COL += 1
    if CUR_COL >= len (COLORS):
        CUR_COL = 0
    return COLORS[CUR_COL]

ms_athletics_feeds = [(f,alternate_color()) for f in MS_SPORTS_CALENDARS]
hs_athletic_feeds = [(f,alternate_color()) for f in HS_SPORTS_CALENDARS]

parse_icalendar_feed.write_feeds_to_gdoc(
    '0B-fhMzqaF6ywaF9YWFlDVUxucEU',
    ms_athletics_feeds)
parse_icalendar_feed.write_feeds_to_gdoc(
    '0B-fhMzqaF6ywTVRKMktlaWZOejQ',
    hs_athletic_feeds)


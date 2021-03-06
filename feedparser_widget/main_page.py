import parse_feeds
#if 'everything is broken':
#    print "ACK EVERYTHING IS BROKEN"
#else:
import gdoc_writer
import os.path
from parse_feeds import Feed

all_feeds = [
    Feed(url='http://www.innovationcharter.org/health-office/health-office-updates/posts.xml',title_prefix='Health Office:'),
    Feed(url='http://www.innovationcharter.org/theater/theater-updates/posts.xml',title_prefix='Theater:'),    
    ]

ms_feeds = [        Feed(url='http://www.innovationcharter.org/middle-school/academic-program/yearbook/announcement/posts.xml',title_prefix='MS Yearbook:'),
        Feed(url='http://www.innovationcharter.org/middle-school/ms-updates/posts.xml',title_prefix='MS:'),
]

hs_feeds = [        Feed(url='http://www.innovationcharter.org/high-school/hs-updates/posts.xml',title_prefix='HS:'),
                    ]

ms_sports_main_feed = [    Feed(url='http://www.innovationcharter.org/middle-school/athletics/mssportsannouncements/posts.xml',title_prefix='MS Sports:'),
    ]

ms_sports_feeds = [
    Feed(url='http://www.innovationcharter.org/high-school/athletics/high-school-athletics-announcements/hs-wrestling/posts.xml',
         title_prefix='Wrestling:'),    
    Feed(url='http://www.innovationcharter.org/middle-school/athletics/mssportsannouncements/ms-varsity-boys-basketball/posts.xml',title_prefix='MS Varsity Boys BBall:'),
    Feed(url='http://www.innovationcharter.org/middle-school/athletics/mssportsannouncements/ms-jv-boys-basketball/posts.xml',title_prefix='MS JV Boys BBall:'),
    Feed(url='http://www.innovationcharter.org/middle-school/athletics/mssportsannouncements/ms-varsity-girls-basketball/posts.xml',title_prefix='MS Varsity Girls BBall:'),
    Feed(url='http://www.innovationcharter.org/middle-school/athletics/mssportsannouncements/ms-jv-girls-basketball/posts.xml',title_prefix='MS JV Girls BBall:'),
    Feed(url='http://www.innovationcharter.org/middle-school/athletics/mssportsannouncements/ms-cross-country-announcements/posts.xml',title_prefix='MS XC:'),
    Feed(url='http://www.innovationcharter.org/middle-school/athletics/mssportsannouncements/ms-boys-soccer-announcements/posts.xml',title_prefix='MS Boys Soccer:'),
    Feed(url='http://www.innovationcharter.org/middle-school/athletics/mssportsannouncements/ms-girls-soccer-announcements/posts.xml',title_prefix='MS Girls Soccer:'),

    
    ]

hs_sports_main_feed = [
    Feed(url='http://www.innovationcharter.org/high-school/athletics/high-school-athletics-announcements/posts.xml',
         title_prefix='HS:'),
    ]

hs_sports_feeds = [
    Feed(url='http://www.innovationcharter.org/high-school/athletics/high-school-athletics-announcements/hs-wrestling/posts.xml',
         title_prefix='Wrestling:'),
    Feed(url='http://www.innovationcharter.org/high-school/athletics/high-school-athletics-announcements/hs-cheerleading/posts.xml',
         title_prefix='HS Cheer:'),
    Feed(url='http://www.innovationcharter.org/high-school/athletics/high-school-athletics-announcements/hs-jv-boys-basketball/posts.xml',
         title_prefix='HS JV Boys BBall:'),
    Feed(url='http://www.innovationcharter.org/high-school/athletics/high-school-athletics-announcements/hs-varsity-boys-basketball/posts.xml',
         title_prefix='HS Varsity Boys BBall:'),
    Feed(url='http://www.innovationcharter.org/high-school/athletics/high-school-athletics-announcements/hs-varsity-girls-basketball/posts.xml',
         title_prefix='HS Varsity Boys BBall:'),    
    Feed(url='http://www.innovationcharter.org/high-school/athletics/high-school-athletics-announcements/indoor-track/posts.xml',
         title_prefix='Indoor Track:'),
    Feed(url='http://www.innovationcharter.org/high-school/athletics/high-school-athletics-announcements/boys-varsity-soccer-announcements/posts.xml',
         title_prefix='HS Boys Varsity Soccer:'),
    Feed(url='http://www.innovationcharter.org/high-school/athletics/high-school-athletics-announcements/cross-country-announcements/posts.xml',
         title_prefix='HS XC:'),
    Feed(url='http://www.innovationcharter.org/high-school/athletics/high-school-athletics-announcements/girls-varsity-soccer-announcements/posts.xml',
         title_prefix='HS Girls Varsity Soccer:'),
    Feed(url='https://sites.google.com/a/innovationcharter.org/new-website/middle-school/athletics/mssportsannouncements/ms-dance-announcements/posts.xml',title_prefix='Dance:'),
    Feed(url='https://sites.google.com/a/innovationcharter.org/new-website/high-school/athletics/high-school-athletics-announcements/hs-softball-announcements/posts.xml',title_prefix='HS Softball:'),
    Feed(url='https://sites.google.com/a/innovationcharter.org/new-website/high-school/athletics/high-school-athletics-announcements/hs-track-and-field-announcements/posts.xml',title_prefix='HS Track:'),
    ]

data = [
    # Temp HTML file, Resource ID for google drive upload, feed, args to html generator
    ('front.html','0B-fhMzqaF6ywb1dKalJaTkthUWM',
     #ms_feeds + hs_feeds +
     all_feeds + [
         # MS Feeds (we do them by hand here to add limits to numbesr...
        #Feed(url='http://www.innovationcharter.org/middle-school/ms-updates/posts.xml',title_prefix='MS:',max_entries=2),
        #Feed(url='http://www.innovationcharter.org/high-school/hs-updates/posts.xml',title_prefix='HS:',max_entries=2),
        Feed(url='http://www.innovationcharter.org/news/press/all-school-updates/posts.xml',title_prefix=''),
        #Feed(url='http://www.innovationcharter.org/news/press/board-updates/posts.xml',title_prefix='Board:',
         #max_days=6),
        ], {'shown_initially':4,'total_limit':8}),
    ('ms.html','0B-fhMzqaF6ywNHR6a09nS0VJV2M',ms_feeds + all_feeds +[Feed(url='http://www.innovationcharter.org/middle-school/academic-program/yearbook/announcement/posts.xml',title_prefix='MS Yearbook:',max_entries=1)],
     {'shown_initially':4,'total_limit':8}),
    ('hs.html','0B-fhMzqaF6ywU0VGTnZCN2ZteHM',hs_feeds + all_feeds,
     {'shown_initially':4,'total_limit':8}),
    ('main_sports.html','0B-fhMzqaF6ywWWwxQ05xb0tTa1k',hs_sports_feeds + ms_sports_feeds + hs_sports_main_feed + ms_sports_main_feed,{'shown_initially':3,'total_limit':8}),
    ('ms_sports.html',  '0B-fhMzqaF6ywZlJIQ2RmTXd1ZEE',ms_sports_main_feed + ms_sports_feeds,{'shown_initially':3,'total_limit':8}),
    ('hs_sports.html',  '0B-fhMzqaF6ywVDV1eDdwYVdMOFE',hs_sports_main_feed + hs_sports_feeds,{'shown_initially':3,'total_limit':8}),
    ('hs_sports_main.html', '0B-fhMzqaF6ywMHhfTXY2YTVpV0U',hs_sports_main_feed,{'shown_initially':3,'total_limit':8}),
    ('ms_sports_main.html', '0B-fhMzqaF6ywckxaV1pWRU5obHM',ms_sports_main_feed,{'shown_initially':3,'total_limit':8}),    
    ('board.html','0B-fhMzqaF6ywU25PcmRyemNYQmM',[Feed(url='http://www.innovationcharter.org/news/press/board-updates/posts.xml',title_prefix='Board:')], {'shown_initially':4,'total_limit':8}),
    ]

main_updater = os.path.exists('am_main')
BACKUP_AFTER = 7

for filename,resourceid,feeds,entry_kwargs in data:
    if False: # If things are broken and we just need the files
        print 'Parsing feeds for ',filename
        out = parse_feeds.entries_to_html(
            parse_feeds.process_feeds(feeds),**entry_kwargs
            )
        ofi = file(filename,'wb')
        ofi.write(out.encode('utf-8'))
        ofi.close()
    else:
        # Do the normal thing
        if (main_updater or not gdoc_writer.updated_within_last(resourceid,BACKUP_AFTER)):
            print 'Parsing feeds for ',filename
            out = parse_feeds.entries_to_html(
                parse_feeds.process_feeds(feeds),**entry_kwargs
            )
            ofi = file(filename,'wb')
            ofi.write(out.encode('utf-8'))
            ofi.close()
            gdoc_writer.update_resource_from_file(resourceid, filename, mimetype='text/html')
        else:
            print resourceid,"already being updated from elsewhere..."

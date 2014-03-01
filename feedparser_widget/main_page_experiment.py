import parse_feeds_experiment
import gdoc_writer
from parse_feeds import Feed
ms_feeds = [        Feed(url='http://www.innovationcharter.org/middle-school/academic-program/yearbook/announcement/posts.xml',title_prefix='MS Yearbook:'),
        Feed(url='http://www.innovationcharter.org/middle-school/ms-updates/posts.xml',title_prefix='MS:'),
]
hs_feeds = [        Feed(url='http://www.innovationcharter.org/high-school/hs-updates/posts.xml',title_prefix='HS:'),
                    ]
ms_sports_feeds = [
    Feed(url='http://www.innovationcharter.org/middle-school/athletics/mssportsannouncements/ms-varsity-boys-basketball/posts.xml',title_prefix='MS Varsity Boys BBall:'),
    Feed(url='http://www.innovationcharter.org/middle-school/athletics/mssportsannouncements/ms-jv-boys-basketball/posts.xml',title_prefix='MS JV Boys BBall:'),
    Feed(url='http://www.innovationcharter.org/middle-school/athletics/mssportsannouncements/ms-varsity-girls-basketball/posts.xml',title_prefix='MS Varsity Girls BBall:'),
    Feed(url='http://www.innovationcharter.org/middle-school/athletics/mssportsannouncements/ms-jv-girls-basketball/posts.xml',title_prefix='MS JV Girls BBall:'),
    Feed(url='http://www.innovationcharter.org/middle-school/athletics/mssportsannouncements/ms-cross-country-announcements/posts.xml',title_prefix='MS XC:'),
    Feed(url='http://www.innovationcharter.org/middle-school/athletics/mssportsannouncements/ms-boys-soccer-announcements/posts.xml',title_prefix='MS Boys Soccer:'),
    Feed(url='http://www.innovationcharter.org/middle-school/athletics/mssportsannouncements/ms-girls-soccer-announcements/posts.xml',title_prefix='MS Girls Soccer:'),
    Feed(url='http://www.innovationcharter.org/middle-school/athletics/mssportsannouncements/ms-volleyball-announcements/posts.xml',title_prefix='MS Volleyball:'),
    Feed(url='http://www.innovationcharter.org/middle-school/athletics/mssportsannouncements/posts.xml',title_prefix='MS Sports:'),
    Feed(url='http://www.innovationcharter.org/middle-school/athletics/mssportsannouncements/indoor-track-and-field/posts.xml',title_prefix='MS Indoor Track:'),
    Feed(url='http://www.innovationcharter.org/middle-school/athletics/mssportsannouncements/ms-cheerleading/posts.xml',title_prefix='MS Cheer:'),
    ]
hs_sports_feeds = [
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
    Feed(url='http://www.innovationcharter.org/high-school/athletics/high-school-athletics-announcements/posts.xml',
         title_prefix='HS:'),
    ]

data = [
    # Temp HTML file, Resource ID for google drive upload, feed, args to html generator
    ('new_file.html','0B-fhMzqaF6ywYVdLLWVSSmpSRVk',ms_sports_feeds,{'shown_initially':7,'total_limit':15,}),
    ]

for filename,resourceid,feeds,entry_kwargs in data:
    print 'Parsing feeds for ',filename
    out = parse_feeds_experiment.entries_to_html(
        parse_feeds_experiment.process_feeds(feeds),**entry_kwargs
        )
    ofi = file(filename,'wb')
    ofi.write(out.encode('utf-8'))
    ofi.close()
    gdoc_writer.update_resource_from_file(resourceid, filename, mimetype='text/html')

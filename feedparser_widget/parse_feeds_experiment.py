import feedparser, re, time,types, calendar

def gmtime_to_localtime (gm_time_struct):
    seconds = calendar.timegm(gm_time_struct)
    return time.localtime(seconds) # Return local time structure

all_results = []

class Feed:

    max_entries = 4
    remove_magic = u'-'
    one_day_magic = u'*'
    max_days = 0
    title_prefix = u''
    
    def __init__ (self, **kwargs):
        self.__done_parsing =  False
        for k,v in kwargs.items():
            setattr(self,k,v)

    def parse (self):
        if self.__done_parsing:
            return
        self.parsed = feedparser.parse(self.url)
        self.parsed.entries.sort(key=lambda x: x.published_parsed, reverse=True)
        self.entries = self.parsed.entries
        if self.max_days:
            self.entries = filter(
                lambda e: time.time() - time.mktime(e.published_parsed) < (60 * 60 * 24 * self.max_days),
                self.entries
                )
        if self.one_day_magic:
            self.entries = filter(
                lambda e: not (
                                    (e.title and e.title[0] == e.title[-1] == self.one_day_magic) and 
                                    time.time() - time.mktime(e.published_parsed) > (60*60*24)
                                    ),
                self.entries
                )
        if self.remove_magic:
                self.entries = filter(
                        lambda e: not (e.title and e.title[0] == e.title[-1] == self.remove_magic),
                        self.entries
                        )
        if self.max_entries:
                self.entries = self.entries[:self.max_entries] # Trim our list...
        if self.title_prefix:
                for e in self.entries:
                        e['title'] = self.title_prefix + u' ' + e['title']
        self.__done_parsing = True                     
                                   
def clean_content (entry):
    '''Return content with no color or other formatting information included.'''
    content = unicode(entry['content'][0]['value'])
    for pat,repl in [
            (u'\xa0','&nbsp;'),
            (u'(line-height|color|background|font-family|font-size|margin-[topbmleftright]*):[^;"]*([;"])',u'\\2'),
            (u'</?font[^>]*>',''),
            (u'<a ',u'<a target="_top" '),
            ]:
        content = re.sub(pat,repl,content)
    return content

def close_open_tags (markup_string):
    assert(type(markup_string) in types.StringTypes)
    open_tags = []
    in_tag = False
    tagname = u''
    n = 0
    while n < len(markup_string):
        char = markup_string[n]
        if in_tag:
            if in_tag == True: # First character after <
                if char == u'/':
                    in_tag = u'CLOSE'
                else:
                    in_tag = u'OPEN'
                tagname = u'' # End if / first char after <
            if char in u' >\t\n': # If we're done with the tagname
                if in_tag == u'OPEN':
                    open_tags.append(tagname)
                if in_tag == u'CLOSE' and open_tags: # End of close tag...
                    if tagname.lower() == open_tags[-1].lower():
                        open_tags = open_tags[:-1] # remove closed tag from list of open tags...
                    else: # Otherwise we have invalid xml and we'll ignore
                        i = 2
                        while i < len(open_tags) and tagname.lower() != open_tags[-i].lower():
                            i += 1
                        if open_tags[-i].lower() == tagname.lower():
                            open_tags = open_tags[:-i] # We've closed off multiple elements
                        #else:
                        #    print u'INVALID XML - IGNORING CLOSETAG %s'%tagname
                    tagname = u''
                in_tag = False
            else:
                if char != u'/':
                    tagname = tagname + char
        else:
            if char == u'<':
                in_tag = True
        n += 1
    # Now that we're done...
    open_tags.reverse()
    closed_tags = u''.join([u'</%s>'%t for t in open_tags])
    if in_tag:
        i = 1
        while markup_string[-i] != u'<':
            i += 1
        markup_string = markup_string[:-i]
    return markup_string + closed_tags

def trim_at_line_length (markup_string, lines=5, chars_per_line=45):
    assert(type(markup_string) in types.StringTypes)
    line_length = 0
    char_length = 0
    open_tags = []
    in_tag = False
    tagname = u''
    i = 0
    while i < len(markup_string):
        if line_length >= lines:
            if in_tag:
                while i < len(markup_string) and markup_string[i] != '<':
                    i -= 1 # Get out of tag first
            else:
                while i < len(markup_string) and  markup_string[i] not in' \n\t>':
                    i -= 1
            return close_open_tags(markup_string[:i]+'&hellip;')
        char = markup_string[i]
        if in_tag:
            if in_tag == True: # First character after <
                if char == '/':
                    in_tag = 'CLOSE'
                else:
                    in_tag = 'OPEN'
                tagname = '' # End if / first char after <
            if char in ' >\t\n': # If we're done with the tagname
                if in_tag == 'OPEN':
                    if tagname == 'br':
                        line_length += 1
                        char_length = 0
                    open_tags.append(tagname)
                if in_tag == 'CLOSE' and open_tags: # End of close tag...
                    if tagname.lower() == open_tags[-1].lower():
                        open_tags = open_tags[:-1] # remove closed tag from list of open tags...
                        if tagname in ['br','div','p','li','tr']:
                            if tagname == 'br':
                                line_length += 1
                                char_length = 0
                            elif char_length: # If there are any characters sitting in a block-level, add a line
                                line_length += 1
                                char_length = 0
                    else: # Otherwise we have invalid xml and we'll ignore
                        n = 2
                        while n < len(open_tags) and tagname.lower() != open_tags[-n].lower():
                            n += 1
                        if (len(open_tags) > i) and open_tags[-i].lower() == tagname.lower():
                            open_tags = open_tags[:-n] # We've closed off multiple elements
                        #else:
                        #    print 'INVALID XML - IGNORING CLOSETAG %s'%tagname
                    tagname = ''
                if char == '>':
                    in_tag = False
                else:
                    in_tag = 'PASTTAGNAME'
            else:
                if in_tag != 'PASTTAGNAME' and char != '/':
                    tagname = tagname + char
        else:
            if char == '<':
                in_tag = True
            else: # Now we're in non-tag content... !
                char_length += 1
                if char_length > chars_per_line:
                    line_length += 1
                    char_length = 0
        i += 1
    # Now that we're done...

    return markup_string
    
def trim_at_line_length_broken (text,lines=5,chars_per_line=45):
    i = 0
    nchars = 0
    nlines = 0
    in_tag = False
    open_tags = []
    tagname = ''
    while i < len(text):
        char = text[i]
        if char == '<':
            in_tag = True
        elif char == '>':
            in_tag = False
            tagname = ''
        elif in_tag:
            if char not in [' \t\n']:
                if char == '>':
                    in_tag = False
                elif in_tag != 2:
                    tagname += char
                if tagname in ['br','div','p','blockquote','li','tr']:
                    if tagname not in open_tags:
                        nlines += 1
                        nchars = 0
            else: # Otherwise the character *is* a space...
                if tagname in open_tags: # Note -- we store the close-tag name for this to work
                    open_tags.remove(tagname) # Close out a tag...
                else:
                    open_tags.append('/' + tagname) # store the close-tag name...
                in_tag = 2 # Special marker to not count this as a tagname...
        elif not in_tag:
            nchars += 1
            if nchars > chars_per_line:
                nlines += 1
                nchars = 0
        if nlines > lines:
            return close_open_tags(text[:i]+'&hellip;')
        i += 1
    if in_tag:
        i = 1
        while i > len(text) and text[-i] != '<':
            i += 1
        if i < len(text):           
            text = text[:-i]
    return close_open_tags(text)
            
def process_feeds (feeds, total_limit=10):
        all_entries = []
        for f in feeds:
            f.parse()
            all_entries.extend(f.entries)
        all_entries.sort(key=lambda x: x.published_parsed, reverse=True)
        if total_limit:
                all_entries = all_entries[:total_limit]
        return all_entries

def entry_to_html (entry, line_limit=5, chars_per_line=45):
        content = trim_at_line_length(
                clean_content(entry), lines=line_limit,chars_per_line=chars_per_line
                )
        link = entry.link
        # Google sites convenience hack
        link = link.replace('https://sites.google.com/a/innovationcharter.org/new-website/',
                            'http://www.innovationcharter.org/')
        date = time.strftime('Published %A, %b %d, %I:%M%p',gmtime_to_localtime(entry['published_parsed']))
        if entry['published_parsed']==entry['updated_parsed']:
                if time.strftime('%A%b%d',entry['updated_parsed'])==time.strftime('%A%b%d',entry['published_parsed']):
                        # If same day, just mention updated time
                        if time.strftime('%I%M%p',entry['updated_parsed']) != time.strftime('%I%M%p',entry['published_parsed']):
                                date = date + time.strftime('(Updated %I:%M%p)',gmtime_to_localtime(entry['updated_parsed']))
                else:
                        date = date + time.strftime('(Updated %A, %b %d, %I:%M%p)',gmtime_to_localtime(entry['updated_parsed']))
        return '''<div class="entry"><h3><a target="_top" href="%(link)s">%(title)s</a></h3>
         <div class="entry_content">
                     %(content)s
         </div>
         <div class="datestamp">%(date)s</div>
        </div>'''%{'link':link, 'title':entry.title,'content':content,'date':date}

def entries_to_html (entries, total_limit=10, shown_initially=5):
        header_file = file('html_head.html','r')
        footer_file = file('html_foot.html','r')
        html_out = header_file.read(); header_file.close()
        html_out = html_out + '<div class="top_entries">'
        for e in entries[:shown_initially]:
                html_out = html_out + entry_to_html(e)
        html_out = html_out + '</div>'
        extras = entries[shown_initially:]
        if extras:
                html_out += '''
                <div class="control"><a id="more" href="#" onclick="show()">Show more...</a></div>
                <div id="hidden_entries" class="hidden_entries">'''
                for e in extras:
                        html_out = html_out + entry_to_html(e)
                html_out += '''<div class="control"><a id="less" href="#" onclick="hide()">Show less...</a></div>
                        </div>'''
        html_out += footer_file.read()
        footer_file.close()
        return html_out

# Try this out...
#parised = feedparser.parse(feed_url)
#print close_open_tags(clean_content(parsed.entries[0])[:500])
if __name__ == '__main__':
        feeds = [
                Feed(url="http://www.innovationcharter.org/news/press/all-school-updates/posts.xml",
                title_prefix='Board:'),
                #Feed(url=u'http://www.innovationcharter.org/theater/theater-updates/posts.xml',title_prefix='Theater:'),
                #Feed(url='http://www.innovationcharter.org/high-school/athletics/high-school-athletics-announcements/boys-varsity-soccer-announcements/posts.xml',title_prefix='Varsity:'),
                ]
        e = process_feeds(feeds)
        out = entries_to_html(e,shown_initially=len(e)-1)
        ofi = file('/tmp/test.html','wb')
        ofi.write(out.encode('utf-8'))
        ofi.close()

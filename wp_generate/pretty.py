
import re
import html

from html.parser import HTMLParser
from bs4.dammit import EntitySubstitution

#
# This *almost* work well with PHP and entity refs
# but *actually* this class treat part of PHP as
# CDATA and additional space between entity refs
# and other data things...probably, need PHP pre
# processor for this to work correctly.
#
class HTMLPrettify(HTMLParser):

    def __init__(self):
        super().__init__()
        self.stack = []
        self.html = ''
        self.pre = False
        self.tabs = '\t'
        self.escaper = EntitySubstitution()
        self.convert_charrefs = False

    # dirty but (probably) works!
    def escape(self, text):
        def escape_php(match):
            php = html.escape(match.group('php'))
            return '<?php{}?>'.format(php)        
        regex = re.compile('<\?php(?P<php>(?! \?>)[^\x00]*?)\?>')
        return regex.sub(escape_php, text)

    def unescape(self, text):
        def unescape_php(match):
            php = html.unescape(match.group('php'))
            return '<?php{}?>'.format(php)
        regex = re.compile('<\?php(?P<php>(?! \?>)[^\x00]*?)\?>')
        return regex.sub(unescape_php, text)

    def pretty(self, html):
        html = self.escape(html)
        self.feed(html)
        self.html = self.unescape(self.html)
        return self.html

    def gettab(self):
        if len(self.stack) != 0:
            return self.tabs*len(self.stack)
        else:
            return ''

    def push(self, tag):
        self.stack = [tag] + self.stack

    def pop(self):
        self.stack = self.stack[1:]

    def top(self):
        return self.stack[0]

    def write(self, html, noline=True, noindent=False):
        if noline and noindent:
            self.html += html
        elif noindent:
            self.html += html + '\n'
        elif noline:
            self.html += self.gettab() + html
        else:
            self.html += self.gettab() + html + '\n'

    def handle_starttag(self, tag, attrs):
        attr = ''.join([' {}="{}"'.format(k,v) for k,v in attrs])
        self.write('<' + tag + attr + '>', False)
        if tag not in ['meta']:
            self.push(tag)
        if tag == 'pre':
            self.pre = True
                        
    def handle_endtag(self, tag):
        self.pop()
        self.write('</' + tag + '>', False)
        if tag == 'pre':
            self.pre = False

    def handle_startendtag(self, tag, attrs):
        attr = ''.join([' {}="{}"'.format(k,v) for k,v in attrs])
        self.write('<' + tag + attr + '/>', False, True)

    def handle_comment(self, data):
        self.write('<!-- {} -->'.format(data), False)

    def handle_data(self, data):
        if not self.pre:
            #data = self.escaper.substitute_html(data)
            data = re.sub(r'\s+', ' ', data)
            if data != ' ':
                self.write(data, False, False)
        else:
            self.write(data)

    def handle_entityref(self, name):
        if not self.pre:
            self.write('&{};'.format(name.strip()), False)

    def handle_charref(self, name):
        if not self.pre:
            self.write('&#{};'.format(name.strip()), False)

    def handle_decl(self, name):
        self.write('<!' + name + '>', False)

    def handle_pi(self, data):
        if data.startswith('php'):
            data = re.sub('\n', '\n' + self.gettab(), data)
        self.write('<?' + data + '>', False)
    
    def unknown_decl(self, name):
        self.log('unknown decl:' + name)
        self.write('<!' + name + '>', False)
        

if __name__ == '__main__':

    PHP='''
    <header class="page-header">
        <h1 class="page-title">
            <?php
            /* translators: %s: search query. */
            printf( esc_html__( 'Search Results for: %s', 'underscore' ), '<span>' . get_search_query() . '</span>' );
            ?>
        </h1>
    </header><!-- .page-header -->
    '''
    print(HTMLPrettify().pretty(PHP))

    


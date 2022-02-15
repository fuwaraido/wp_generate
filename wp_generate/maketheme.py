
import re
import os
import html
import configparser
import json

from pathlib import Path
from jinja2 import evalcontextfilter, Environment, FileSystemLoader
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from pretty import HTMLPrettify

import distutils
from distutils import dir_util

# "do nothing" handler
class NullHandler:

    def write(self, html): pass
    def close(self): pass
    def handle_starttag(self, tag, attrs): pass
    def handle_endtag(self, name): pass
    def handle_startendtag(self, tag, attrs): pass
    def handle_data(self, data): pass
    def handle_entityref(self, name): pass
    def handle_charref(self, name): pass
    def handle_decl(self, name): pass
    def handle_pi(self, data): pass    
    def unknown_decl(self, name): pass

# template output handler
class TemplateHandler:

    def __init__(self, filename, template_imports, coding='utf-8'):
        self.filename = filename
        self.template_imports = template_imports
        self.set_html_lang = True
        self.set_body_class = True
        self.set_meta_charset = True
        self.set_article_id = True
        self.tag_formatter = {}
        self.fd = self.open(filename, coding)
        self.init_template()
        self.init_formatter()
        self.log('start generation:' + filename)

    def open(self, filename, coding):
        dirname = os.path.split(filename)[0]
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        return open(filename, 'w', encoding=coding)

    def log(self, message):
        print(message)

    def write(self, html):
        self.fd.write(html)

    def close(self):
        self.fd.close()

    def init_formatter(self):
        if self.set_html_lang:
            self.add_formatter('html', self.format_html)            
        if self.set_body_class:
            self.add_formatter('body', self.format_body)            
        if self.set_meta_charset:
            self.add_formatter('meta', self.format_meta)
        if self.set_article_id:
            self.add_formatter('article', self.format_article)

    def init_template(self):
        for inc in self.template_imports:
            self.write('{{% import "{}" as php %}}'.format(inc))

    def add_formatter(self, tag, filt_func):
        self.tag_formatter[tag] = filt_func

    def format_attrs(self, attrs):
        return ''.join([' {}="{}"'.format(k,v) for k,v in attrs])

    def format_html(self, tag, attrs):
        return '<html lang="{{ php.html_lang() }}">'

    def format_body(self, tag, attrs):
        return '<body class="{{ php.body_class() }}">'

    def format_meta(self, tag, attrs):
        dic = dict(attrs)
        if 'charset' in dic: dic['charset'] = '{{ php.meta_charset() }}'
        return '<meta' + self.format_attrs(dic.items()) + '>'

    def format_article(self, tag, attrs):
        dic = dict(attrs)
        if dic['id'].startswith('post'):
            dic['id'] = 'post-<?php the_ID(); ?>'
            dic['class'] = '<?php post_class(); ?>'
        return '<article' + self.format_attrs(dic.items()) + '>'
        
    def handle_starttag(self, tag, attrs):
        if tag in self.tag_formatter:
            self.write(self.tag_formatter[tag](tag, attrs))
        else:
            self.write('<' + tag + self.format_attrs(attrs) + '>')

    def handle_endtag(self, tag):        
        self.write('</' + tag + '>')

    def handle_startendtag(self, tag, attrs):
        if tag in self.tag_formatter:
            self.write(self.tag_formatter[tag](tag, attrs))
        else:
            self.write('<' + tag + self.format_attrs(attrs) + '>')

    def handle_data(self, data):
        self.write(data)

    def handle_entityref(self, name):
        self.write('&{};'.format(name))

    def handle_charref(self, name):
        self.write('&#{};'.format(name))

    def handle_decl(self, name):
        self.write('<!' + name + '>')

    def handle_pi(self, data):
        self.write('<?' + data + '>')
    
    def unknown_decl(self, name):
        self.log('unknown decl:' + name)
        self.write('<!' + name + '>')

class Instruction:

    INSTRUCTIONS = [
        '%BEGIN', # %BEGIN: "filename"
        '%END', # %END: "filename" (optional)
        '%SKIP', # %SKIP
        '%BLOCK', # %BLOCK: "blockname"
        '%END_BLOCK', # %ENDBLOCK: "blockname"(optional)
        '%INLINE', # %INLINE: "macroname"        
        '%END_INLINE',
        '%CODE', # %CODE: one-liner
        '%PAGE', # %PAGE: page-settings
        # conditionals are not implemented yet!
        '%IF',
        '%ELSE',
        '%END_IF'
    ]

    # regex matches *any* real numbers...1, 100, .5, 0.5, 1.0e3, 1.0e-2...etc
    REAL_NUMBER = re.compile('[+-]?(?:\d+\.?\d*|\.\d+)(?:(?:[eE][+-]?\d+)|(?:\*10\^[+-]?\d+))?')

    @classmethod
    def decomp_page_params(cls, params):
        def set_type(value):
            if value == 'None':
                return None
            elif value == 'True' or value == 'False':
                return bool(value)
            elif value[0] == "'" and value[-1] == "'":
                return str(value[1:-1])
            elif cls.REAL_NUMBER.match(value):
                return float(value)
            else: # probably symbols but not supported yet!
                raise ValueError('incorrect type in %PAGE:' + value)

        print(params)

        # decompose tokens and convert value types
        tokens = [s.strip().split('=') for s in re.split(r',', params)]
        values = [set_type(t[1].strip()) for t in tokens]
        keys = [t[0].strip() for t in tokens]
        
        # return parameters as dictionary
        return dict(zip(keys, values))
    
    @classmethod
    def parse(cls, cmd):
        tokens = cmd.split(':')

        # ignore upper/lower cases
        tokens[0] = tokens[0].upper()
        
        if not tokens[0] in cls.INSTRUCTIONS:
            raise Exception('Invalid instruction:{}'.format(cmd))
        
        if tokens[0] == '%BEGIN':            
            params = dict([('cmd', 'BEGIN'), ('filename', tokens[1].strip(' "'))])
        elif tokens[0] == '%END':
            params = dict([('cmd', 'END')])
        elif tokens[0] == '%SKIP':
            params = dict([('cmd', 'SKIP')])
        elif tokens[0] == '%BLOCK':
            params = dict([('cmd', 'BLOCK'), ('blockname', tokens[1].strip(' "'))])
        elif tokens[0] == '%END_BLOCK':
            params = dict([('cmd', 'END_BLOCK')])
        elif tokens[0] == '%INLINE':
            params = dict([('cmd', 'INLINE'), ('macroname', tokens[1].strip(' "'))])
        elif tokens[0] == '%END_INLINE':
            params = dict([('cmd', 'END_INLINE')])
        elif tokens[0] == '%CODE':
            params = dict([('cmd', 'CODE'), ('macroname', tokens[1].strip(' "'))])
        elif tokens[0] == '%PAGE':
            params = dict([('cmd', 'PAGE'), ('params', cls.decomp_page_params(tokens[1]))])
        # conditionals are not implemented yet!
        elif tokens[0] == '%IF':
            params = dict([('cmd', 'IF'), ('cond', tokens[1])])
        elif tokens[0] == '%ELSE':
            params = dict([('cmd', 'ELSE')])
        elif tokens[0] == '%END_IF':
            params = dict([('cmd', 'END_IF')])
        elif tokens[0] == '%SET':
            params = dict([('cmd', 'SET'), ('value', tokens[1])])

        return Instruction(params)

    def __init__(self, params):
        self.params = params

    def __getitem__(self, name):
        return self.params[name]

##
## TemplateGenerator main class
##
## This class generate .jinja template from .html
##
class TemplateGenerator(HTMLParser):

    def __init__(self, theme_template_dir, template_dir, template_imports):
        super().__init__()
        self.handler = []
        self.template_imports = template_imports
        self.convert_charrefs = False
        self.push(NullHandler())
        self.theme_template_dir = theme_template_dir
        self.template_dir = template_dir
        self.page_info = None
        
    def push(self, handler):
        self.handler = [handler] + self.handler

    def pop(self):
        self.handler[0].close()
        self.handler = self.handler[1:]

    def top(self):
        return self.handler[0]

    def handle_starttag(self, tag, attrs):
        self.top().handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        self.top().handle_endtag(tag)

    def handle_startendtag(self, tag, attrs):
        self.top().handle_startendtag(tag, attrs)

    def handle_data(self, data):
        self.top().handle_data(data)

    def handle_entityref(self, name):
        self.top().handle_entityref(name)

    def handle_charref(self, name):
        self.top().handle_charref(name)

    def handle_decl(self, name):
        self.top().handle_decl(name)

    def handle_pi(self, data):
        self.top().handle_pi(data)

    def unknown_decl(self, data):
        self.top().unknown_decl(data)

    def handle_comment(self, data):
        data = data.strip()
        if data.startswith('%'):
            instr = Instruction.parse(data)
            if instr['cmd'] == 'BEGIN':
                filename = os.path.join(self.theme_template_dir, instr['filename'])
                self.push(TemplateHandler(filename.replace('\\','/'), self.template_imports))
            elif instr['cmd'] == 'END':
                self.pop()
            elif instr['cmd'] == 'SKIP':
                self.push(NullHandler())
            elif instr['cmd'] == 'BLOCK':
                self.top().write('{% block ' + instr['blockname'] + ' %}')
            elif instr['cmd'] == 'END_BLOCK':
                self.top().write('{% endblock %}')                
            elif instr['cmd'] == 'INLINE':
                self.top().write('{{ ' + instr['macroname'] + ' }}')
                self.push(NullHandler())
            elif instr['cmd'] == 'END_INLINE':
                self.pop()
            elif instr['cmd'] == 'CODE':
                self.top().write('{{ ' + instr['macroname'] + ' }}')
            elif instr['cmd'] == 'PAGE':
                self.page_info = instr['params']
            else:
                raise Exception("Unknown instruction")
        else:
            self.top().write('<!-- ' + data + ' -->')
   
    def generate(self, filename):
        with open(os.path.join(self.template_dir, filename), encoding='utf-8') as f:
            print("fetch:" + str(filename))
            self.page_info = None # clear page info
            self.feed(f.read())


##
## theme generation
##

PHP_COMMENT='''<?php
/**
 *
 * {}
 *
 * @link: {}
 *
 * @package: {}
*/
'''

PHP_HEADER='''get_header();
?>\n'''

PHP_FOOTER='''
<?php
get_sidebar();
get_footer();
?>'''

class PHPFileTemplate:

    def __init__(self, theme_name, theme_desc, theme_link):
        self.theme_name = theme_name
        self.theme_desc = theme_desc
        self.theme_link = theme_link

    def create(self, filename, content, is_main, coding='utf-8'):
        with open(filename, 'w', encoding=coding) as f:
            f.write(PHP_COMMENT.format(
                self.theme_desc, self.theme_link, self.theme_name))
            if is_main:
                f.write(PHP_HEADER)
            else:
                f.write('?>\n')
            f.write(content)
            if is_main:
                f.write(PHP_FOOTER)

##
## ThemeGenerator class
##
## This class generate .php files from .jinja template
##
class ThemeGenerator:

    def __init__(self, theme_template_dir, php_file):
        self.theme_template_dir = theme_template_dir
        self.php_file = php_file
        self.page_info = {}        
        self.main_templates = ['index.php',
                               'single.php',
                               'singular.php',
                               'page.php',
                               'search.php',
                               'archive.php',
                               'category.php']

    def add_page_info(self, outfile, page_info):
        self.page_info[outfile] = page_info

    def locate_templates(self, theme_template_dir, theme_dir):
        names = []
        for root, dirs, file in os.walk(theme_template_dir):
            for f in file:                
                if f.endswith('jinja') and not f.startswith('_'):
                    source = os.path.join(os.path.relpath(root, theme_template_dir), f)
                    subdir = os.path.relpath(root, theme_template_dir)
                    target = os.path.join(os.path.join(theme_dir, subdir), f)
                    names.append((os.path.normpath(source),
                                  os.path.normpath(Path(target).with_suffix('.php'))))
        return names

    # render template into .php file
    def render_template(self, template, outfile, **kwargs):
        is_main = os.path.split(outfile)[1] in self.main_templates
        html = HTMLPrettify().pretty(template.render(**kwargs))
        self.php_file.create(outfile, html, is_main, 'utf-8')

    def generate(self, theme_dir, **kwargs):
        # initialize jinja2
        file_loader = FileSystemLoader(self.theme_template_dir)
        env = Environment(loader=file_loader)
        env.filters['quote'] = lambda s: "'{}'".format(s)
        env.filters['php'] = lambda s: "<?php {} ?>".format(s)

        # determine template locations
        names = self.locate_templates(self.theme_template_dir, theme_dir)

        # generate .php for each .jinja
        for infile, outfile in names:
            infile = infile.replace('\\', '/') # jinja doesn't work with \\
            print(infile, "=>", outfile)

            # create directory if not exists
            if not os.path.isdir(os.path.split(outfile)[0]):
                os.makedirs(os.path.split(outfile)[0])
            
            page_name = os.path.split(outfile)[1]
            if page_name in self.page_info:
                page = self.page_info[page_name]
                if 'template' in page:
                    page['base_template'] = infile
                    template = env.get_template(page['template'])
                    self.render_template(template, outfile, page=page, **kwargs)
                else:
                    template = env.get_template(infile)
                    self.render_template(template, outfile, page=page, **kwargs)
            else:
                template = env.get_template(infile)
                self.render_template(template, outfile, **kwargs)

##
## convert python data to php code
##
def php(ob):
    if type(ob) == list:
        return 'array(' + ', '.join([str(php(e)) for e in ob]) + ')'
    elif type(ob) == dict:
        elems = ['{} => {}'.format(php(k), php(v)) for k,v in ob.items()]
        return 'array(' + ', '.join(elems) + ')'
    elif type(ob) == str:
        return "'{}'".format(ob)
    else:
        return ob

class Link:
    def __init__(self, name, path, version):
        self.name = name
        self.path = path
        self.version = version

class Sidebar(dict):

    def __init__(
        self,        
        id = 'sidebar-1',
        name = 'Sidebar',
        desc = 'Add widgets here',
        before_widget = '<section id="%1$s" class="widget %2$s">',
        after_widget = '</section>',
        before_title = '<h2 class="widget-title">',
        after_title = '</h2>'):
        self['id'] = id
        self['name'] = name
        self['description'] = desc
        self['before_widget'] = before_widget
        self['after_widget'] = after_widget
        self['before_title'] = before_title
        self['after_title'] = after_title

##
## functions.php generation
##
class FunctionsPHP:

    # some wordpress options to generate 
    def __init__(self, theme_template_dir, theme_name, php_file):
        self.theme_template_dir = theme_template_dir
        self.theme = theme_name
        self.php_file = php_file        
        self.text_domain_location = '/languages'        
        self.register_primary_menu = 'Primary'
        self.automatic_feed_links =  True
        self.title_tag = True
        self.post_thumbnails = True
        self.html5 = True
        self.custom_background = {
            'default-color': 'ffffff',
            'default-image': ''
        }
        self.selective_refresh_widgets = True
        self.custom_logo = {
            'height': 250,
            'width': 250,
            'flex-width': True,
            'flex-height': True
        }
        self.sidebar_options = [ dict(Sidebar()) ]
        self.styles = [Link('additional-style', 'css/style.css', '1.0')]
        self.scripts = [Link('additional-script', 'js/script.js', '1.0')]

    def generate(self, theme_dir):        
        file_loader = FileSystemLoader(self.theme_template_dir)
        env = Environment(loader=file_loader)
        env.filters['php'] = php
        template = env.get_template('_functions.php')
        output = template.render(config=self)        
        outfile = os.path.join(theme_dir, 'functions.php')
        self.php_file.create(outfile, output, False, 'utf-8')

##
## some default configs
##
TEMPLATE_IMPORTS=['_common.jinja']
THEME_LINK='https://developer.wordpress.org/themes/basics/template-hierarchy/'
THEME_DESCRIPTION='This is {} theme, generated by Viper wordpress theme generator!'

##
## Core engine
##
class Theme:

    def __init__(self, name):
        # default theme configuration
        self.meta_template_dir = './meta_templates'
        self.template_dir = './' + name + '_template'
        self.template_imports = TEMPLATE_IMPORTS
        self.theme_suffix = '.html'
        self.theme_dir = './' + name
        self.theme_link = THEME_LINK
        self.theme_name = name
        self.theme_template_dir = name + '_meta_template'
        self.theme_description = name + ' theme'
        self.theme_files = []
        self.php_file = PHPFileTemplate(
            self.theme_name,
            self.theme_description,
            self.theme_link)
        self.page_info = {}
        
        # FunctionsPHP configure its default
        self.functions = FunctionsPHP(
            self.theme_template_dir,
            self.theme_name,
            self.php_file)

    def load_config(self, filename):        
        config = configparser.RawConfigParser()        
        config.read(filename)

        def default(section, key, fallback):
            return section[key] if key in section else fallback

        def default_json(section, key, fallback):
            try:
                return json.loads(default(section, key, fallback))
            except Exception:
                raise ValueError("Incorrect value for {}".format(key))
        
        def is_section(section, name):
            return section.startswith(name) or section.startswith(name + '_')

        if 'Template' in config:
            section = config['Template']
            self.meta_template_dir = default(section, 'meta_template_dir', self.meta_template_dir)
            self.template_dir = section['template_dir']
            self.template_imports = default_json(section, 'template_imports', "['_common.jinja']")
            
        if 'Theme' in config:
            section = config['Theme']
            self.theme_name = default(section, 'theme_name', self.theme_name)
            self.theme_suffix = default(section, 'theme_suffix', '.html')
            self.theme_dir = default(section, 'theme_dir', os.path.join('.' + self.theme_name))
            self.theme_link = default(section, 'theme_link', THEME_LINK)
            self.theme_template_dir = default(section, 'theme_template', self.theme_name + '_meta_template')
            self.theme_description = default(section, 'theme_description', THEME_DESCRIPTION.format(self.theme_name))
            self.theme_files = default_json(section, 'theme_files', '[]')

        funcs = self.functions
        if 'Functions' in config:
            section = config['Functions']
            funcs.text_domain_location = default(section, 'text_domain_location', './language')
            funcs.register_primary_menu = default(section, 'register_primary_menu', 'Primary')
            funcs.automatic_feed_links = default_json(section, 'automatic_feed_links', 'true')
            funcs.title_tag = default_json(section, 'title_tag', 'true')
            funcs.post_thumbnails = default_json(section, 'post_thumbnails', 'true')
            funcs.html5 = default_json(section, 'html5', 'true')
            funcs.selective_refresh_widgets = default_json(section, 'selective_refresh_widgets', 'true')

        if 'CustomLogo' in config:
            section = config['CustomLogo']
            funcs.custom_logo['width'] = default_json(section, 'width', '250')
            funcs.custom_logo['height'] = default_json(section, 'height', '250')
            funcs.custom_logo['flex-width'] = default_json(section, 'flex-width', 'true')
            funcs.custom_logo['fiex-height'] = default_json(section, 'flex-height', 'true')

        if 'CustomBackground' in config:
            section = config['CustomBackground']
            funcs.custom_background['default-color'] = default(section, 'default-color', 'ffffff')
            funcs.custom_background['default-image'] = default(section, 'default-image', '')

        ## CSS Script Sidebar section
        sections = config.sections()
        for section in sections:
            if is_section(section, 'CSS'):
                css = config[section]
                funcs.styles += [Link(css['name'], css['location'], css['version'])]
            elif is_section(section, 'Script'):
                js = config[section]
                funcs.styles += [Link(js['name'], js['location'], js['version'])]
            elif is_section(section, 'Sidebar'):
                section = config[section]
                sb = Sidebar()
                sb.id = section['id']
                sb.name = default(section, 'name', sb['name'])
                sb.description = default(section, 'description', sb['description'])
                sb.before_widget = default(section, 'before_widget', sb['before_widget'])
                sb.after_widget = default(section, 'after_widget', sb['after_widget'])
                sb.before_title = default(section, 'before_title', sb['before_title'])
                sb.after_title = default(section, 'after_title', sb['after_title'])

    ## find html files in theme_template_dir
    def locate_theme(self):
        for file in os.listdir(self.template_dir):
            if file.endswith(self.theme_suffix):
                print('template found: {}'.format(file))
                name = Path(os.path.split(file)[1]).with_suffix('')
                self.theme_files.append(name)

    ## generate "meta" template from html
    def generate_meta(self):
        template = TemplateGenerator(
            self.theme_template_dir,
            self.template_dir,
            self.template_imports)

        # copy meta templates
        distutils.dir_util.copy_tree(
            self.meta_template_dir, self.theme_template_dir)
        
        # generate .jinja for each .html
        for name in self.theme_files:
            template.generate(Path(name).with_suffix(self.theme_suffix))
            # if html has %PAGE delective, register it
            if template.page_info:
                self.page_info[str(name)] = template.page_info

    ## generate php theme files
    def generate(self):
        theme = ThemeGenerator(self.theme_template_dir, self.php_file)
        for name, page in self.page_info.items():
            theme.add_page_info(name + '.php', page)
        theme.generate(self.theme_dir)

    ## generate functions.php
    def generate_functions(self):        
        self.functions.generate(self.theme_dir)

if __name__ == '__main__':
    theme = Theme('venom')
    theme.load_config('venom.ini')
    theme.locate_theme()
    theme.generate_meta()
    theme.generate()
    theme.generate_functions()

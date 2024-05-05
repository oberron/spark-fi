# These are the setting for the local machine
# as opposed to publishconf which is for the remote machine

from os.path import abspath, join, pardir
import sys

dp_site_spec = abspath(join(__file__, pardir))
print("debug sitespec", dp_site_spec)
sys.path.append(dp_site_spec)

from site_spec import AUTHOR, SITENAME, SITEURL, SITE_LOGO, ABOUT, SOCIAL, RELATIVE_URLS

# SITEURL not needed if RELATIVE URL set to True
# but SITREURL needed for feed domain
FEED_DOMAIN = SITEURL


SITEMAP = { "format": "xml"}

DELETE_OUTPUT_DIRECTORY = False

PATH = ['content', "notion"]

# Static path relative to PATH
STATIC_PATHS = ["static/img", "static/webvtt"]
OUTPUT_PATH = 'public'
PLUGINS = ['sitemap']
PLUGINS.append('more_categories')

TIMEZONE = 'Europe/Rome'

DEFAULT_LANG = 'en'

# BOILER PLATE for PELICAN-JUPYTER
# from :
# https://github.com/danielfrg/pelican-jupyter

MARKUP = ('md', )

FEED_ALL_ATOM = "feed.xml"
# FEED_ALL_ATOM = None
RSS_FEED_SUMMARY_ONLY = False
# FEED_DOMAIN = ":8000"
FEED_RSS_URL = True
FEED_MAX_ITEMS = 500
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DELETE_OUTPUT_DIRECTORY = False

# Blogroll
LINKS = (('Pelican', 'https://getpelican.com/'),
         ('Python.org', 'https://www.python.org/'),
         ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
         ('You can modify those links in your config file', '#'),)

# Social widget


DEFAULT_PAGINATION = 10

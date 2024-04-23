# These are the setting for the local machine
# as opposed to publishconf which is for the remote machine

from os.path import abspath,join
AUTHOR = 'Oberron'
SITENAME = 'Spark-fi'
# SITEURL not needed if RELATIVE URL set to True
# but SITREURL needed for feed domain
SITEURL = 'http://localhost:8000'
FEED_DOMAIN = SITEURL
RELATIVE_URLS = True
SITE_LOGO = "site_logo.jpg"
ABOUT = "No spark is too small to fire a dream"

SITEMAP = { "format": "xml"}

DELETE_OUTPUT_DIRECTORY = False

PATH = 'content'

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
#FEED_ALL_ATOM = None
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
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10


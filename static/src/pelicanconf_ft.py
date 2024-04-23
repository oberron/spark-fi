# These are the setting for the local machine
# as opposed to publishconf which is for the remote machine

from os.path import abspath,join
AUTHOR = 'Rezpe & Oberron'
SITENAME = 'Touch 4 Tech'
# SITEURL not needed if RELATIVE URL set to True
# but SITREURL needed for feed domain
SITEURL = "https://frenchtouch.dev/"
FEED_DOMAIN = SITEURL
# Uncomment following line if you want document-relative URLs when developing
# if RELATIVE_URLS overrides SITEURL with "." in site content
# but not in feed.xml
RELATIVE_URLS = True

SITE_LOGO = "site_logo.png"
ABOUT = "One brick at a time contributing to the DKIW pyramid fundation"

# RELATIVE_URLS = False
SITEMAP = { "format": "xml"}


DELETE_OUTPUT_DIRECTORY = False

PATH = 'content'
STATIC_PATHS = ["static/img", "static/webvtt"]
OUTPUT_PATH = 'public'
# PLUGINS = ['sitemap', 'pelican-ipynb.markup']
PLUGINS = ['sitemap']
# remove , 'pelican-jupyter' as obsolete, replaced by manual calls to pandoc
# 'more_categories' allows more than 1 category
# https://github.com/pelican-plugins/more-categories/blob/master/example/pelicanconf.py
# pip install pelican-more-categories
PLUGINS.append('more_categories')


TIMEZONE = 'Europe/Rome'

DEFAULT_LANG = 'en'

# BOILER PLATE for PELICAN-JUPYTER
# from :
# https://github.com/danielfrg/pelican-jupyter

MARKUP = ('md', )

# IGNORE_FILES = [".ipynb_checkpoints"]

# END OF BOILER PLATE for PELICAN-JUPYTER

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = "feed.xml" #MCV changed for testing
#FEED_ALL_ATOM = None
RSS_FEED_SUMMARY_ONLY = False

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
SOCIAL = (('Twitter', 'twitter', 'https://twitter.com/frenchtouchdev'),
          ('Youtube', 'youtube', 'https://www.youtube.com/@frenchtouchdev'),
          ('tiktok','tiktok','https://www.tiktok.com/@frenchtouchdev'),
          ('Facebook','facebook-f','https://www.facebook.com/frenchtouch.dev'),
          ('GitHub','github','https://github.com/french-touch/frenchtouch'),
          ("Podcast",'podcast',"https://feeds.soundcloud.com/users/soundcloud:users:404637861/sounds.rss"),
          ("Instagram", "instagram","https://www.instagram.com/frenchtouch.dev/"),
          ("RSS","rss",f"{FEED_DOMAIN}feed.xml"),
          ("Mail","envelope","mailto:tellme@frenchtouch.dev"))

DEFAULT_PAGINATION = 10



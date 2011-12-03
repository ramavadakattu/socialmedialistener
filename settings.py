
from local_settings import *
import os
import logging
import logging.config
from django.conf import global_settings


SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
# Django settings for socialmedialistener project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'appmedia')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/appmedia/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '9&s!kku@qlll35!v3198+_3)is5b!!2t-l8i!!wovf#lgmm83('

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',       
)

ROOT_URLCONF = 'socialmedialistener.urls'

TEMPLATE_DIRS = (os.path.join(SITE_ROOT, 'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.humanize',
    'south',
    'session_messages',
    
    #Internal apps
    'paypallistener',
)


#LOG_FILE_PATH in django
LOG_FILE_PATH = "\""+os.path.join(os.path.dirname(os.path.normpath(__file__)),"logs.txt")+"\""
#LOG FILE NAME In django
LOG_FILE_NAME = os.path.join(os.path.dirname(os.path.normpath(__file__)),'logging.conf')
 
 
#how many shares to make a tory popular
TOPIC_CUTOFF = 14
#how many shares to make a story popular in a top

ebaykeywords = "paypal,ebay"

searchquery = "paypal OR ebay"

NUMBER_OF_TRENDING_TOPICS = 10

excude_topics = ['://bit','http','amp','ebay-store','item','paypal','link','click','something','ebay','new','end','|','auction','payment','sold','price','store','sale','rt','deal','date','(r)','(r']



PAGE_SIZE = 15

#Twitter thread started
twitter_thread = False


trending_time = 3


 
#number of entries to fetch in each crawl
NUMBER_OF_ENTRIES =100

MIN_CUTOFF = 1

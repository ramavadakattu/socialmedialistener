import os, sys
sys.path.append('/home/djangoprojects')
sys.path.append('/home/djangoprojects/socialmedialistener')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socialmedialistener.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
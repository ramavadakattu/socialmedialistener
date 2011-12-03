
from django.core.management import setup_environ
import settings
setup_environ(settings) 


from paypallistener.views import MrCrawler


cmanager = MrCrawler()
print cmanager.isItBelongstoEbay('microplace to outsource their academic work to the lowest bidder ')

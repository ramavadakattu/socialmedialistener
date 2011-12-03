
from django.core.management import setup_environ
import settings
setup_environ(settings) 


from paypallistener.views import MrCrawler


cmanager = MrCrawler()
cmanager.fillSummaryText()

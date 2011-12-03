
from django.core.management import setup_environ
import settings
setup_environ(settings) 


from paypallistener.views import fetchSummaryText,MrCrawler,getBeautyTitle
from topia.termextract import extract


title = getBeautyTitle("#nowplaying- #ebay auction- let's see how many hits we can get- PLEASE RETWEET this-60 bucks for this computer    ")
print title
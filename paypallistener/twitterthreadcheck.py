import urlparse

import logging
import logging.config
import settings
from TwitterManager import TwitterFetcher



mlogger = logging.getLogger(__name__)

class TwitterThreadCheck :
      """
      This thread basically check whether Twitter thread is running or not if not it will start the thread      
      """      
      def process_request(self, request):        
        twitter_thread_started = settings.twitter_thread
        mlogger.debug("IN twitter thread check middleware %s"%(str(settings.twitter_thread),))        
        if twitter_thread_started is True :
            return None
        else :
            pass
            #starte the twitter thread           
            #TwitterFetcher().start()            
            settings.twitter_thread = True
        return None  
        
        
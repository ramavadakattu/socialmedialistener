from paypallistener.views import MrCrawler,TwitterManager
import sys
import traceback
import time
import threading
import logging
import logging.config

mlog=logging.getLogger(__name__) 

class TwitterFetcher(threading.Thread):     
     def __init__(self):          
         threading.Thread.__init__(self)  
           
     def run (self):             
               tmanager = TwitterManager()
               i = 0
               while True :
                try : 
                    tmanager.fetchDataFromTwitter()                    
                    time.sleep(60)
                    i = i+1
                    mlog.debug("how many requests %s" % (str(i),))
                except :
                    exc_info = sys.exc_info()
                    print "######################## Exception #############################"
                    print '\n'.join(traceback.format_exception(*(exc_info or sys.exc_info())))
                    print "################################################################"                    
                    time.sleep(60)
         

  
                
 
 
 
      
         


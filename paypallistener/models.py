from django.db import models
import logging
import logging.config
import settings
import urlparse

from BeautifulSoup import BeautifulSoup , BeautifulStoneSoup
from django.utils.html import strip_tags,urlize

#loading the logging configuration
logging.config.fileConfig(settings.LOG_FILE_NAME,defaults=dict(log_path=settings.LOG_FILE_PATH))
 
#Create module logger 
mlog=logging.getLogger(__name__) 
mlog.debug("From settings LOG_FILE_NAME %s LOG_FILE_PATH %s" % (settings.LOG_FILE_NAME,settings.LOG_FILE_PATH))



class Entry(models.Model):
      url = models.URLField(max_length=1024)
      title = models.CharField(max_length=1024)
      htmltitle = models.CharField(max_length=124,default=None,null=True,blank=True)
      description = models.TextField(null=True,blank=True)
      noofshares = models.IntegerField(default=0)
      service = models.CharField(max_length=20,null=True,blank=True)
      examined = models.BooleanField(default=False)
      #date which says when this got published in friendfeed   
      entry_pdate = models.DateField()
      entry_pdatetime = models.DateTimeField()
      #dates which tells when this got created and updated
      entry_createdon = models.DateTimeField(auto_now_add=True)
      enty_updatedon =  models.DateTimeField(auto_now=True)
      #created gmt time
      entrycreatedgmt = models.DateTimeField(null=True)
      
      twittercount = models.IntegerField(default=0)
      deliciouscount = models.IntegerField(default=0)
      readercount = models.IntegerField(default=0)
      facebookcount = models.IntegerField(default=0)
            
      
      def __unicode__(self):
            return  " %s ---- %s "% (self.url,self.title)
            
      def getDomainName(self):
        host,path = urlparse.urlsplit(self.url)[1:3]
        return host
    
      def getNeatTitle(self):
         from paypallistener.views import getBeautyTitle
         return getBeautyTitle(self.title)      
       
        
#Storing all the entryids related to the above entry
class EntryUIDS(models.Model):
    entry = models.ForeignKey(Entry)
    entryid = models.CharField(db_index=True,max_length=124)
    createdon = models.DateTimeField(auto_now_add=True)
    updatedon =  models.DateTimeField(auto_now=True)
    

  
     
class Stats(models.Model):
    whichcron = models.CharField(max_length=25,null=True,blank=True)
    createdon = models.DateTimeField(auto_now_add=True)
    updatedon =  models.DateTimeField(auto_now=True)
    totalentries = models.IntegerField(null=True,blank=True)
    totalsaved = models.IntegerField(null=True,blank=True)
    howmanymoved = models.IntegerField(null=True,blank=True)
    howmanydeleted = models.IntegerField(null=True,blank=True)
    
    def __unicode__(self):
        return  " %s  "% (self.whichcron,)
        
        
class Xtag(models.Model):
    name = models.CharField(max_length=512)        
    entries = models.ManyToManyField(Entry,null=True,blank=True)
    createdon = models.DateTimeField(auto_now_add=True)
    updatedon =  models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "Tag name %s "% (self.name,)
        
        
class Weight(models.Model):
    xtag = models.ForeignKey(Xtag)
    weight = models.FloatField(null=True,blank=True)
    createdon = models.DateTimeField(auto_now_add=True)
    updatedon =  models.DateTimeField(auto_now=True)
    
    
    def __unicode__(self):
        return "Weight %s "% (str(weight),)
    

class NotEnglish(models.Model):    
    text = models.TextField()
    createdon = models.DateTimeField(auto_now_add=True)
    updatedon =  models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "text %s "% (self.text,)
    
    
    
      
             
            

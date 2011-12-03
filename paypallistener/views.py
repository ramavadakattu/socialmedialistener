# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import logging
import feedparser
import settings
import httplib
import urlparse
import urllib2
import urllib
import unicodedata


from BeautifulSoup import BeautifulSoup , BeautifulStoneSoup
from django.utils.encoding import smart_str, smart_unicode
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.contrib.syndication.feeds import Feed
import sys
from django.utils.html import urlize
from django.db.models import Q
from django.http import HttpResponse , HttpResponseRedirect
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags,urlize
from django.db.models import Avg, Max, Min, Count
from django.utils.html import strip_tags,urlize


import random
import traceback
import sys
from django.template.loader import render_to_string
from django.views.generic.list_detail import object_list
import twitter
from oice.langdet import langdet
from oice.langdet import streams
from oice.langdet import languages
import twython.core as twython
from paypallistener.models import Xtag,Weight,NotEnglish


from StringIO import StringIO

from datetime import datetime
from datetime import timedelta

from paypallistener.models import Entry,EntryUIDS,Stats
from topia.termextract import extract

#module logger use this logger in the standalone functions
mlogger = logging.getLogger(__name__)



            
    
def getStoriesByTag(request,tagid):
    tagid = long(tagid)
    tag = Xtag.objects.get(id=tagid)
    ntag = tag.name.replace("-"," ")
    entries = tag.entries.filter(noofshares__gte=settings.MIN_CUTOFF).order_by('-enty_updatedon')[0:settings.PAGE_SIZE]
    trendingtopics = getTrendingTopics()
    totalentries = EntryUIDS.objects.all().count() 
    return render_to_response("tag_data.html", {'totalentries':totalentries,'entries':entries,'trendingtopics':trendingtopics,'tag':tag,'ntag':ntag}, RequestContext(request))
   


def showPopularStories(request,pageno=1):   
    paginator = Paginator(Entry.objects.filter(noofshares__gte = settings.TOPIC_CUTOFF).order_by('-entry_createdon'),settings.PAGE_SIZE)              
    popularentries =  paginator.page(pageno)
    trendingtopics = []
    #  trendingtopics = getTrendingTopics()
    totalentries = EntryUIDS.objects.all().count()     
    return render_to_response("index.html", {'totalentries':totalentries,'popularentries':popularentries,'trendingtopics':trendingtopics}, RequestContext(request))
   
   
def deleteInvalidEntries():    
    todaygmt = datetime.utcnow()   
    three_days = timedelta(days=2)              
    dthreedatetime = todaygmt - three_days
    n_delete = Entry.objects.filter(noofshares__lte=settings.MIN_CUTOFF,entry_createdon__lte =  dthreedatetime).count()
    mlogger.debug("total to be delete %d" %(n_delete,))
    Entry.objects.filter(noofshares__lte=settings.MIN_CUTOFF,entry_createdon__lte =  dthreedatetime).delete() 
   
    
   
def getTotalShares(request):    
    d = {}

    try:
            if request.method == "GET" :                 
                totalentries = EntryUIDS.objects.all().count()
                d['totalentries'] = totalentries
    except:
        d['error'] = "oops........some problem at the server end"
    
    json = simplejson.dumps(d)
    return HttpResponse(json)  
    
    
def getTrendingTopics():
     #calculate the datetime 3 hours before
    fewhoursbefore = datetime.utcnow()-timedelta(hours=settings.trending_time) 
    
    #substract trending time from the above    
    trending_topics =Xtag.objects.filter(updatedon__gte=fewhoursbefore,weight__createdon__gte=fewhoursbefore).exclude(name__in=settings.excude_topics).annotate(total_weight=Count('weight')).order_by('-total_weight')[:settings.NUMBER_OF_TRENDING_TOPICS]
    trending_topics = list(trending_topics)
    removelist = []
    for topic in trending_topics :
        topic.name = topic.name.replace("-"," ")
        if (len(topic.name) <= 1):
            removelist.append(topic)
            
    for topic in removelist :
        trending_topics.remove(topic)         
   
    return trending_topics    
    
    
class  MrCrawler:
    
    def __init__(self):
        self.logger = logging.getLogger('%s.%s' % (__name__,self.__class__.__name__))
        
        
    def fillSummaryText(self):
        entries = Entry.objects.filter(noofshares__gte = settings.TOPIC_CUTOFF,examined=False).order_by('-entry_createdon')
        for entry in entries :
            (summary_text,title) = fetchSummaryText(entry.url)
            mlogger.debug("Summary text = %s title = %s " %(summary_text,title))
            if summary_text is not None :
                entry.description = summary_text
                
            if title is not None :
                entry.htmltitle = title
            
            entry.examined = True
            entry.save()
            
  
    def triggerfetchFeed(self):
        ebaykeywords = settings.ebaykeywords
        for word in ebaykeywords.split(",") :
            self.fetchFeed(word)        
        
        
    def fetchFeed(self,word):         
         stat= Stats()
         service = "temp"
         self.logger.info("Entering fetch feed function") 
         self.logger.info("fetching the feed from the friend feed")         
         querystring =  word+" "+"service:googlereader,delicious,facebook"
         data ={}
         data['q'] = querystring
         data['num'] = 100
         data['format'] =  "json"
         url_values = urllib.urlencode(data)
         url = "http://friendfeed-api.com/v2/search"          
         response = urllib2.urlopen(url+"?"+url_values)        
         d = simplejson.loads(response.read())
         
         self.logger.debug("how many entries %s" %len(d['entries']))
         stat.totalentries =  len(d['entries'])
         savedentries  =  0
         #for each entry fetch its title and url
         self.logger.info("iterating filtering the feed entries and saving it to the database")
        
         for entry in d['entries']:
                    try:
                       
                        service = entry['via']['name']                      
                        body = entry['body']
                        btitle = body
                        
                    
                        #if this entry belongs to ebay keywords then only proceed other wise not
                        #if self.isItBelongstoEbay(unicode(body)) is False :
                        #   continue  
                        #check whether this entry id is already present
                        entrylist =  EntryUIDS.objects.filter(entryid__exact=str(entry['id']))
                        if len(entrylist)  > 0 :
                           self.logger.debug("entry id already present....Skip don't save in the database..continue..."+str(entry['id']))
                           continue
                        else:
                           self.logger.debug("entry id not present..trying to save into the database"+str(entry['id']))
                           
                        mainlinks = []
                       
                       
                        #for converting html &amp; characters
                        soup = BeautifulSoup(urlize(body),convertEntities=BeautifulStoneSoup.HTML_ENTITIES)                           
                        mainlinks = soup.findAll("a")
                        self.logger.debug("total number of link associated with this tweet %s"%(str(len(mainlinks))))
                        
                       
                        
                        for mlink in mainlinks :                           
                            twitterlink = mlink['href']                   
                             
                            #self.isItInEnglish(btitle) 
                            if(self.isItInEnglish(btitle)) :   
                                burl  = self.bringBaseUrl(twitterlink)
                                self.logger.debug("Base URL is (after eliminating the redirecting url's)  %s" % burl)
                                
                                if burl is None :
                                    continue
                              
                                if (self.isitFaceBookUrl(burl) ):
                                    continue
                               
                               
                                if burl :
                                             self.logger.debug("preparing the Entry object")
                                             newsentrylist = Entry.objects.filter(url=burl)
                                             self.logger.debug("length of newslist %s" % len(newsentrylist))
                                             if len(newsentrylist) > 0 :
                                                  self.logger.debug("There is news entry with this URL  checking for duplicates......... ")                                                                                  
                                                  oldentry = newsentrylist[0]                                             
                                                  oldentry.noofshares = oldentry.noofshares  + 1                                                  
                                                  
                                                
                                                  if service == "Facebook" :
                                                        oldentry.facebookcount = oldentry.facebookcount +1 
                                                    
                                                  if service == "Google Reader":
                                                        oldentry.readercount =  oldentry.readercount + 1
                                                    
                                                  if service == "delicious" :
                                                        oldentry.deliciouscount = oldentry.deliciouscount + 1
                                                    
                        
                                                  oldentry.save()
                                                  noteDownTags(btitle,oldentry)
                                                  entryUID = EntryUIDS()
                                                  entryUID.entryid = str(entry['id'])
                                                  entryUID.entry = oldentry
                                                  entryUID.save()                                                 
                                                  savedentries = savedentries+1
                                                  
                                             else :
                                                  #creates a new entry now
                                                  self.logger.debug("There is no news entry with this URL so saving this")
                                                   #form an entry object
                                                  ne = Entry()
                                                  topic = None                            
                                                  ne.service = service                                             
                                                  ne.title = btitle
                                                  ne.url = burl                                                  
                                               
                                                  #preprocess the title
                                                  if service == "Facebook" :
                                                        ne.facebookcount = 1 
                                                    
                                                  if service == "Google Reader":
                                                        ne.readercount =  1
                                                    
                                                  if service == "delicious" :
                                                        ne.deliciouscount = 1
                                                    
                                                 
                                                  ne.noofshares = 1
                                                  #self.logger.debug("published_parsed  date from universal feed parser %s" %entry.published_parsed)
                                                  #year,month,day,hour,min,second,asd,asdfk,asdfd = entry.published_parsed
                                                  dt = datetime.strptime(entry['date'],"%Y-%m-%dT%H:%M:%SZ")                                                   
                                                  ne.entry_pdate = dt.date()
                                                  ne.entry_pdatetime = dt
                                                  self.logger.debug("publisheddate = %s pdate = %s" %(ne.entry_pdate,ne.entry_pdatetime))
                                                  ne.entrycreatedgmt = datetime.utcnow()
                                                
                                                  ne.save()
                                                  noteDownTags(btitle,ne)
                                                  entryUID = EntryUIDS()
                                                  entryUID.entryid = str(entry['id'])
                                                  entryUID.entry = ne
                                                  entryUID.save()                                                                                                       
                                                  savedentries = savedentries+1  
                                                          
                    except :                       
                        mlogger.debug("some error skipping this entyr and  continue")                      
                        exc_info = sys.exc_info()
                        print "-------------------Exception-----------------------------------"
                        print '\n'.join(traceback.format_exception(*(exc_info or sys.exc_info())))
                        print "----------------------------------------------------------------"

            
         stat.whichcron = "generic"   
         self.logger.debug("Total entries save = %s" % (str(savedentries),))                           
         stat.totalsaved  =   savedentries
         stat.save()
            
    
    
    #if the base url is pointing to facebook status message don't store that
    def isitFaceBookUrl(self,burl):
         if burl : 
            if burl.find("www.facebook.com/common/browser.php")  >  0:
                                       self.logger.debug("It is a facebook url")
                                       return True  
                                   
            if burl.find("www.facebook.com/profile.php")  >  0:
                                       self.logger.debug("It si a facebook url")
                                       return True
         return False                         
                                
    
    #get title from the body
    #cut down until the first <a>
    def getTitle(self,text):        
        index = text.find("<a")
        
        if index == -1 or index == 0 :
            return text
        elif index > 0 :
            return text[:index+1]
            
        return text
        
 
    #All topics which were found in the text          
    def isItBelongstoEbay(self,text):
        topiclist = []
        ebaykeywords = settings.ebaykeywords
        #self.logger.info("finding the topic for the given text %s" %(text,))
        ntext = text.lower().strip()
        if len(ntext) <= 0 :
            return  topiclist        
        
        
        strings = ebaykeywords.split(",")
        for string in strings :
               
               #self.logger.debug("String = "+string)
                
                if len(string.strip()) <= 0 :
                    continue              
                
                found = True
                prefound = False
                for word in string.split():
                    nword = word.lower().strip()
                
                    if nword in ntext.split() :
                        prevfound = True
                    else :
                        prevfound = False
                    found = found and prevfound
                        
                
                if found :
                    return True
        
        return False 
    
    
    
    
    def bringBaseUrl(self,url):
        ''' returns the base url of the string '''        
        maxattempts = 10
        turl = url
        while (maxattempts  >  0) :               
            host,path,query,hashtag = urlparse.urlsplit(turl)[1:5]
            self.logger.debug("what is the url=%s" % turl)
            self.logger.debug("what is the host %s and path is %s query = %s hashtag = %s"%(host,path,query,hashtag))
            if  len(host.strip()) == 0 :
                return None
            try: 
                connection = httplib.HTTPConnection(host,timeout=10)
                restofurl = path
                if (len(query.strip()) > 0 ):
                    restofurl = restofurl+'?'+query
                    
                if (len(hashtag.strip()) > 0 ):
                    restofurl = restofurl+'#'+hashtag
                
                self.logger.debug("RestofURL = %s" %(restofurl,))
                connection.request("GET",restofurl)
                resp = connection.getresponse()
            except:                         
                return None                     
            maxattempts = maxattempts - 1
            self.logger.debug("state = %d"%resp.status)
            if (resp.status >= 300) and (resp.status <= 399):
                turl = resp.getheader('location')
            elif (resp.status >= 200) and (resp.status <= 299) :
                return turl
            else :
                #some problem with this url
                return None               
        return None

          
        
        
   
        
    def isItInEnglish(self,title):
          self.logger.debug("checking whether the title is in english or not")
          count = 0
          for c in title:
               if ord(c) > 128 :
                    self.logger.debug("c = %s , interger = %d" %(c,ord(c)))
                    count = count +1                                          
           
          if count > 4 :         
                n = NotEnglish()
                n.text = title
                n.save()
                return False
          else :
                return True                
                
          return True        
          ''' try:           
            title = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore')
            title = unicode(title)
            text = streams.Stream(StringIO(title))
            lang = langdet.LanguageDetector.detect(text)
            if  lang == languages.spanish:
                return False
            elif lang == languages.english:
                 return True
          except :
            exc_info = sys.exc_info()
            print "=================Exception============================="
            print '\n'.join(traceback.format_exception(*(exc_info or sys.exc_info())))
            print "----------------------------------------------------------------"
            return True          
              
          return True  '''
            
       

 
 
    def fetchTitle(self,url):
        mlogger.debug("fetching title")
        title = None
        try:
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page,convertEntities=BeautifulStoneSoup.HTML_ENTITIES) 
            titleTag = soup.findAll('title')
            titlesoup = BeautifulSoup(titleTag[0].renderContents(),convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
            title = ''.join([e for e in titlesoup.recursiveChildGenerator() if isinstance(e,unicode)])
            mlogger.debug("what is the title ="+title)
            if len(title) > 0 :
                return title
            else:
                return None
        except:
            mlogger.debug(str(sys.exc_info()[0]))
            return None    
    

def noteDownTags(text,entry):
    newtext = getBeautyTitle(text)
    mlogger.debug("added tag successfully....................")
    extractor = extract.TermExtractor()
    extractor = extract.TermExtractor(extractor.tagger)
    #extractor.filter = extract.permissiveFilter
    extractor.filter = extract.DefaultFilter(singleStrengthMinOccur=1)
    terms  =  extractor(newtext)
    
    for term in terms :
        refinedterm =  term[0].lower().replace(" ","-")
        results = Xtag.objects.filter(name=refinedterm)
        thetag = None        
        if results :
            firsttag = results[0]            
            firsttag.entries.add(entry)            
            firsttag.save()
            #add weight information
            thetag = firsttag
            
        else :
            newtag = Xtag()
            newtag.name = refinedterm            
            newtag.save()
            newtag.entries.add(entry)
            thetag = newtag
            #add weight information
        w = Weight()
        w.xtag = thetag
        w.weight == 1
        w.save()            
                
            

def getBeautyTitle(body):
     text = strip_tags(body)
     temptext = ""
     #remove all the links
     soup = BeautifulSoup(urlize(text))
     for link in soup.findAll("a"):
               link.extract()
            
     newtext = soup.__unicode__().replace("."," ").strip()
     ishypen = newtext.rfind("-")
            
     #for removing the last hypen associated with words
     if ishypen == -1 :
         temptext = newtext
     elif ishypen+1 == len(newtext) :
         temptext = newtext[:ishypen]
     else :
         temptext = newtext
              
              
     #remove tags  , @ symbols etc.........from the tweet
     words = temptext.split()
     finaltext = ""
          
     for word in words:
        newword = word.strip()
        if len(newword) > 0 :
            if newword[0] == "#":
                continue
             
            if newword[0] == "@":
                continue
                
            if newword.lower() == "rt":
                continue
              
            finaltext = finaltext + newword + " "
        
          
     finaltext = finaltext.strip()
          
     if len(finaltext)  == 0 :
              return "Title missing"
            
     if finaltext[0] == "-":
        return finaltext[1:] 
     
            
            
     return finaltext
                


#returns summarytext and title 
def fetchSummaryText(url):    
    mlogger.debug("fetching summary text")
    
    title = None
    try:
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page,convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
        #find all p tags
        allPTags =  soup.findAll('p')
        titleTag = soup.findAll('title')
        titlesoup = BeautifulSoup(titleTag[0].renderContents(),convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
        title = ''.join([e for e in titlesoup.recursiveChildGenerator() if isinstance(e,unicode)])
        mlogger.debug("what is the title ="+title)
        
        for aP in allPTags :
           psoup =  BeautifulSoup(aP.renderContents(),convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
           ptext = ''.join([e for e in psoup.recursiveChildGenerator() if isinstance(e,unicode)])
           #mlogger.debug("render contents="+aP.renderContents())
           #mlogger.debug("ptext ="+ptext)
                     
           if properContainer(ptext) :
                totalwords = len(ptext.split())
                result = anchortest(aP.renderContents(),totalwords,"P");
                mlogger.debug("what is the value of result="+str(result))            
                if result :
                    mlogger.debug("summarized text= %s" % ptext)
                    #if greater than 48 words pass only 48 tokens
                    if len(ptext.split())  >= 48 :
                        nsumtext =  ' '.join(ptext.split()[0:47])
                        nsumtext = nsumtext + " ...."
                        return (nsumtext,title)
                    else :
                        return (ptext,title)
                else :
                    continue
                
        #now search for div tags
        allDivTags =  soup.findAll('div')
        for aDiv in allDivTags :
            dsoup = BeautifulSoup(aDiv.renderContents(),convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
            dtext = ''.join([e for e in dsoup.recursiveChildGenerator() if isinstance(e,unicode)])
            
            if properContainer(dtext) :
                totalwords = len(dtext.split())
                result = anchortest(aDiv.renderContents(),totalwords,"DIV");
                mlogger.debug("what is the value of result="+str(result))            
                if result :
                    mlogger.debug("summarized text= %s" % dtext)
                    #if greater than 48 words pass only 48 tokens
                    if len(dtext.split())  >= 48 :
                        nsumtext =  ' '.join(ptext.split()[0:47])
                        nsumtext = nsumtext + " ...."
                        return (nsumtext,title)
                    else :
                        return (dtext,title)
                else :
                    continue
                
                
        return (None,None)
        
    except:             
        mlogger.debug(str(sys.exc_info()[0]))
        return (None,title)
    
def properContainer(ptext) :
            tokens = ptext.split()
            if len(tokens) <= 21 :
                return False    
            if ptext.find("<!--") >= 0 :
                return False
            if ptext.find("google_ad_client") >= 0 :
                return False
            if (ptext.find("document.") >= 0)  or (ptext.find("window.") >= 0)  :
                return False
            if (ptext.find("=") >= 0) :
                return False
            if (ptext.find("==") >= 0) :
                return False
            if (ptext.find(":") >= 0)  or (ptext.find("{") >= 0) or  (ptext.find("}") >= 0) :
                return False
            
            return True
  
    
    
def anchortest(containerhtml,totalwords,whichcontainer):
    percentage = 65
    awords = 0
    soup = BeautifulSoup(containerhtml)
    allATags =  soup.findAll('a')
    for atag in allATags :
         asoup =  BeautifulSoup(atag.renderContents())
         atext = ' '.join([e for e in asoup.recursiveChildGenerator() if isinstance(e,unicode)])
         awords = awords + len(atext.split())
    
    alloptionTags =  soup.findAll('option')
    for aoption  in  alloptionTags :
        osoup =  BeautifulSoup(aoption.renderContents())
        otext = ' '.join([e for e in osoup.recursiveChildGenerator() if isinstance(e,unicode)])
        awords = awords + len(otext.split())
         
    mlogger.debug("how many totalwords =%d  awords =%d" % (totalwords,awords))
    if awords == 0 :
        awords = 1
    howmuch = (float(awords)/float(totalwords)) * 100
    mlogger.debug("what is the value of howmuch= %d"% howmuch)
    
    if howmuch >= percentage :
        #dont; consider as summary text
        return False
    else :
        #conider as summary text
        return True
    
   

class TwitterManager():
    
     def __init__(self):
        self.logger = logging.getLogger('%s.%s' % (__name__,self.__class__.__name__))


     def fetchDataFromTwitter(self):
        stat= Stats()
        stat.whichcron = "twitter"
        savedentries = 0
        self.logger.debug("Fetching data from twitter")
        params = urllib.urlencode({'q':settings.searchquery,'lang': 'en', 'rpp': 100})
        data={}
        data['q'] = settings.searchquery
        data['lang'] = 'en'
        data['rpp'] = 100
        url_values = urllib.urlencode(data)        
        url = "http://search.twitter.com/search.json"         
        response = urllib2.urlopen(url+"?"+url_values)               
        d = simplejson.loads(response.read()) 
        self.logger.debug("Total entries %s"%(str(len(d['results']))))
        stat.totalentries =  len(d['results'])
        for entry in d['results'] :
            try:
                        tweet = entry['text']
                        btitle = tweet
                        cmanager = MrCrawler()
                        #if this entry belongs to ebay keywords then only proceed other wise not
                        #if cmanager.isItBelongstoEbay(unicode(tweet)) is False :
                        #    continue  
                        #check whether this entry id is already present
                        entrylist =  EntryUIDS.objects.filter(entryid__exact=str(entry['id']))
                        if len(entrylist)  > 0 :
                           self.logger.debug("entry id already present....Skip don't save in the database..continue..."+str(entry['id']))
                           continue
                        else:
                           self.logger.debug("entry id not present..trying to save into the database"+str(entry['id']))
                           
                        mainlinks = []
                       
                       
                        #for converting html &amp; characters
                        soup = BeautifulSoup(urlize(tweet),convertEntities=BeautifulStoneSoup.HTML_ENTITIES)                           
                        mainlinks = soup.findAll("a")
                        self.logger.debug("total number of link associated with this tweet %s"%(str(len(mainlinks))))
                        
                        linkhead = ''                                            
                        linkhead = unicode(tweet)                        
                        
                        for mlink in mainlinks :                           
                            twitterlink = mlink['href']
                            
                            
                             #cmanager.isItInEnglish(linkhead)
                            if(True) :   
                                burl  = cmanager.bringBaseUrl(twitterlink)
                                self.logger.debug("Base URL is (after eliminating the redirecting url's)  %s" % burl)
                                
                                if (cmanager.isitFaceBookUrl(burl) ):
                                    continue
                               
                                if burl :
                                             self.logger.debug("preparing the Entry object")
                                             newsentrylist = Entry.objects.filter(url=burl)
                                             self.logger.debug("length of newslist %s" % len(newsentrylist))
                                             if len(newsentrylist) > 0 :
                                                  self.logger.debug("There is news entry with this URL  checking for duplicates......... ")                                                                                  
                                                  oldentry = newsentrylist[0]                                             
                                                  oldentry.noofshares = oldentry.noofshares  + 1
                                                  oldentry.twittercount = oldentry.twittercount + 1
                                                  oldentry.save()
                                                  noteDownTags(btitle,oldentry)
                                                  entryUID = EntryUIDS()
                                                  entryUID.entryid = str(entry['id'])
                                                  entryUID.entry = oldentry
                                                  entryUID.save()
                                                  savedentries = savedentries+1
                                                  
                                             else :
                                                  #creates a new entry now
                                                  self.logger.debug("There is no news entry with this URL so saving this")
                                                   #form an entry object
                                                  ne = Entry()
                                                  topic = None                            
                                                  ne.service = "twitter"                                              
                                                  ne.title = btitle
                                                  ne.url = burl                                                  
                                                  #preprocess the title
                                                  #
                                                  if(True) :
                                                       ne.noofshares = 1                                                  
                                                       #self.logger.debug("published_parsed  date from universal feed parser %s" %entry.published_parsed)
                                                       #year,month,day,hour,min,second,asd,asdfk,asdfd = entry.published_parsed
                                                       dt = datetime.strptime(entry['created_at'],"%a, %d %b %Y %H:%M:%S +0000")                                                   
                                                       ne.entry_pdate = dt.date()
                                                       ne.entry_pdatetime = dt
                                                       self.logger.debug("publisheddate = %s pdate = %s" %(ne.entry_pdate,ne.entry_pdatetime))
                                                       ne.entrycreatedgmt = datetime.utcnow()
                                                       ne.twittercount = 1
                                                       ne.save()
                                                       noteDownTags(btitle,ne)
                                                       entryUID = EntryUIDS()
                                                       entryUID.entryid = str(entry['id'])
                                                       entryUID.entry = ne
                                                       entryUID.save()                                                                                                       
                                                       savedentries = savedentries+1            
            except :
                        mlogger.debug("some error skipping this entyr and  continue")                      
                        exc_info = sys.exc_info()
                        print "-------------------Exception-----------------------------------"
                        print '\n'.join(traceback.format_exception(*(exc_info or sys.exc_info())))
                        print "----------------------------------------------------------------"

            
            
        self.logger.debug("Total entries save = %s" % (str(savedentries),))                           
        stat.totalsaved  =   savedentries
        stat.save()

    
    
'''
self.logger.info("Bringing down the base URL")
          maxattempts = 5
          turl = url
          while (maxattempts  >  0) :
            self.logger.debug("what is the url=%s" % turl)
            host,path = urlparse.urlsplit(turl)[1:3]
            if  len(host.strip()) == 0 :
               return None
            #self.logger.debug("what is the host %s and path is %s"%(host,path))
            try: 
                    connection = httplib.HTTPConnection(host,timeout=10)
                    connection.request("HEAD", path)
                    resp = connection.getresponse()
                    #attempted
            except:
                     self.logger.debug("Could not open socket some network exception")
                     return None                     
            maxattempts = maxattempts - 1
            if (resp.status >= 300) and (resp.status <= 399):
                self.logger.debug("The present %s is a redirection one" %turl)
                turl = resp.getheader('location')
            elif (resp.status >= 200) and (resp.status <= 299) :
                self.logger.debug("The present url %s is a proper one" %turl)
                return turl
            else :
                #some problem with this url
                return None               
          return None
        '''


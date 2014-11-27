from scrapy.spider import BaseSpider
from scrapy.spider import Spider
from scrapy.contrib.spiders import SitemapSpider
from scrapy.selector import Selector
import re
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url
from scrapy.http import Request
from urlparse import urljoin
#from MedHelp_code.items import QItem
#from MedHelp_code.items import CItem
#from MedHelp_code.items import ForumItem
from WebMD_code.items import QCItem

class GetSeeds(BaseSpider):
    name="seeds"
    def __init__(self, filename=None):
        if filename:
            self.start_urls.append(filename)
    allowed_domains = ['webmd.com']
    start_urls = []
    def parse(self,response):
        sel = Selector(response)
        namelist = sel.xpath('//div[@class="resultlist"]/h4/text()|//div[@class="resultlist"]/ul/li/a/text()').extract()
        linklist = sel.xpath('//div[@class="resultlist"]/h4/text()|//div[@class="resultlist"]/ul/li/a/@href').extract()
        topic=""
        for i in range(0,len(namelist)):
            if namelist[i]==linklist[i]:
                topic=namelist[i]
            else:
                print topic.strip()+">"+namelist[i].strip()+">http://exchanges.webmd.com"+linklist[i].strip()
        return

class ExpSeeds(BaseSpider):
    name="expseeds"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                if i != '':
                    self.start_urls.append(i.split('>')[2].strip())
    allowed_domains=['webmd.com']
    start_urls = []
    def parse(self, response):
        sel = Selector(response)
        if len(sel.xpath('//div[@class="feedHeaderLinks_fmt"]/a[./text()="Discussions"]/@href').extract())>0:
            Dlink = "http://exchanges.webmd.com"+sel.xpath('//div[@class="feedHeaderLinks_fmt"]/a[./text()="Discussions"]/@href').extract()[0]
            print response.url.strip()+">"+Dlink.strip()
        if len(sel.xpath('//div[@class="feedHeaderLinks_fmt"]/a[./text()="Tips"]/@href').extract())>0:
            Tlink = "http://exchanges.webmd.com"+sel.xpath('//div[@class="feedHeaderLinks_fmt"]/a[./text()="Tips"]/@href').extract()[0]
            print response.url.strip()+">"+Tlink.strip()
        if len(sel.xpath('//div[@class="feedHeaderLinks_fmt"]/a[./text()="Resources"]/@href').extract())>0:
            Rlink = "http://exchanges.webmd.com"+sel.xpath('//div[@class="feedHeaderLinks_fmt"]/a[./text()="Resources"]/@href').extract()[0]
            print response.url.strip()+">"+Rlink.strip()
        return

class GetQuestionsCommentsAmount(BaseSpider):
    name="questionsCommentsAmount"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                if i != '':
                    self.start_urls.append(i.split('>')[1])
    allowed_domains = ['webmd.com']
    start_urls = []
    def parse(self,response):
        sel = Selector(response)
        postulrlist = sel.xpath('//div[@class="expert_fmt"]/span[@class="thread_fmt"]/a/@href').extract()
        commentlist = sel.xpath('//div[@class="bottomlinks_fmt"]/a[@class="replynum"]/text()').extract()
        commentAmount = 0
        for i in commentlist:
            commentAmount += int(i.split(' ')[0])
        baseurl = response.url
        if '?pg=' in baseurl:
            baseurl=baseurl.split('?')[0]
        else:
            pass 
        print baseurl.strip()+">%d>%d"%(len(postulrlist),commentAmount)
        
        nextl = sel.xpath('//a[@onclick="wmdTrack(\'he-pagenum_next\');"]/@href').extract()
        if len(nextl)>0:
            nextp=nextl[0]
            baseurl = response.url
            if '?pg=' in baseurl:
                baseurl=baseurl.split('?')[0]
            else:
                pass
            nexturl=urljoin(baseurl,nextp)
            return Request(nexturl, callback=self.parse)
        else:
            pass
        return

class GetQuestions(BaseSpider):
    name="getqs"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                if i != '':
                    self.start_urls.append(i.split('>')[1])
    allowed_domains = ['webmd.com']
    start_urls = []
    def parse(self,response):
        sel = Selector(response)
        #item = QItem()
        qlistnum = len(sel.xpath('//div[@class="expert_fmt"]/span[@class="thread_fmt"]/a/@href').extract())
        if qlistnum>0:
            for i in range(qlistnum):
                question = sel.xpath('//div[@class="discussionx_fmt exchange-reply-container"]/div[@class="expert_fmt"]/div[@id="fulltext%d"]/span[@class="post_fmt"]/text()'%(i+1)).extract()
                if len(question)>0:
                    questiondic={}
                    questiondic[response.url.strip()]=''.join(question)
                    print questiondic
                    #if response.url.strip() in item.keys():
                        #item[response.url.strip()].append(''.join(question))
                    #else:
                        #item[response.url.strip()] = [''.join(question)]
        nextl = sel.xpath('//a[@onclick="wmdTrack(\'he-pagenum_next\');"]/@href').extract()
        if len(nextl)>0:
            nextp=nextl[0]
            baseurl = response.url
            if '?pg=' in baseurl:
                baseurl=baseurl.split('?')[0]
            else:
                pass
            nexturl=urljoin(baseurl,nextp)
            return Request(nexturl, callback=self.parse)
        else:
            pass
        return

class GetQuestionsComments_url(BaseSpider):
    name="questionsCommentsURL"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                if i != '':
                    self.start_urls.append(i.split('>')[1])
    allowed_domains = ['webmd.com']
    start_urls = []
    def parse(self,response):
        sel = Selector(response)
        urlList=sel.xpath('//div[@class="discussionx_fmt exchange-reply-container"]/div[@class="expert_fmt"]/div[@class="bottomlinks_fmt"]/a[1]/@href').extract()
        if len(urlList) >0:
            for i in urlList:
                print response.url.strip()+">"+i.strip()
        nextl = sel.xpath('//a[@onclick="wmdTrack(\'he-pagenum_next\');"]/@href').extract()
        if len(nextl)>0:
            nextp=nextl[0]
            baseurl = response.url
            if '?pg=' in baseurl:
                baseurl=baseurl.split('?')[0]
            else:
                pass
            nexturl=urljoin(baseurl,nextp)
            return Request(nexturl, callback=self.parse)
        else:
            pass
        return


class GetQuestionsComments_url_ex(BaseSpider):
    name="questionsCommentsURLEX"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                if i != '':
                    self.start_urls.append(i.split('>')[1])
    allowed_domains = ['webmd.com']
    start_urls = []
    def parse(self,response):
        sel = Selector(response)
        urlList=sel.xpath('//div[@class="pagination_bottom"]/div[@class="pages"]/a[@onclick="ctrs(\'srb-tpage_last\');"]/@href').extract()
        if len(urlList) >0:
            lastpage = int(urlList[0].split('=')[1])
            for i in range(lastpage):
                n=i+1
                if n==1:
                    print response.url
                elif n >=2:
                    print response.url+'?pg=%d'%n   
                else:
                    pass
        else:
            print response.url
        return


class GetQuestionsComments_c(BaseSpider):        
    name="questionsCommentsContent"
    def __init__(self, filename=None):
        if filename:
            data = open(filename).read().split("\n")
            for i in data:
                if i != '':
                    #self.start_urls.append(i.split('>')[1])
                    self.start_urls.append(i.strip())
    allowed_domains = ['webmd.com']
    start_urls = []
    def parse(self,response):
        sel = Selector(response)
        item = QCItem()
        item['forumid'] = []
        item['questionTitle'] = {}
        item['questionContent'] = {}
        item['commentContent'] = {}
        
        item['questionMaker'] = {}
        item['commentMaker'] = {}
        item['commentMaker'][response.url.strip()] = []
        item['commentReceiver'] = {}
        item['commentReceiver'][response.url.strip()] = []
        item['commentRecvID'] = {}
        item['commentRecvID'][response.url.strip()] = []
        
        item['questionTime'] = {}
        item['commentTime'] = {}
        item['commentTime'][response.url.strip()] = []
        
        item['commentID'] = {}
        
        item['forumid'].append(response.url.strip())
        item['questionTitle'][response.url.strip()]=''.join(sel.xpath('//div[@class="exchange_form_dtr_index_rdr exchange-reply-container"]/div[@class="firstitem_mid_fmt"]/div[@class="first_item_title_fmt"]/text()').extract()).strip()
        
        if len(sel.xpath('//div[@class="firstitem_mid_fmt"]/div[@class="exchange_thread_rdr"]/div[@class="thread_fmt"]/div[@class="post_hdr_fmt"]/a/@href').extract()) > 0:
            item['questionMaker'][response.url.strip()] = sel.xpath('//div[@class="firstitem_mid_fmt"]/div[@class="exchange_thread_rdr"]/div[@class="thread_fmt"]/div[@class="post_hdr_fmt"]/a/@href').extract()[0]
        else:
            item['questionMaker'][response.url.strip()] = "UnknownQuestionMaker"
            
        if len(sel.xpath('//div[@class="firstitem_mid_fmt"]/div[@class="first_posted_fmt"]/script/text()').extract())>0:
            item['questionTime'][response.url.strip()] = sel.xpath('//div[@class="firstitem_mid_fmt"]/div[@class="first_posted_fmt"]/script/text()').extract()[0]
        else:
            item['questionTime'][response.url.strip()] = "UnknownQuestionTime"
        
        item['questionContent'][response.url.strip()] = ''.join(sel.xpath('//div[@class="firstitem_mid_fmt"]/div[@class="exchange_thread_rdr"]/div[@class="thread_fmt"]/div[@class="post_fmt"]/text()').extract()).strip()
        item['commentContent'][response.url.strip()] = []
        item['commentID'][response.url.strip()] = []
        #item['commentContent'][response.url.strip()].append(''.join(sel.xpath('//div[@class="exchange_thread_reply_rdr exchange-reply-container"]/div[@class="thread_fmt"]/div[@class="post_fmt"]/text()|//div[@class="exchange_thread_reply_rdr exchange-reply-container"]/div[@class="thread_fmt"]/div[@class="post_fmt"]/a/text()').extract()).strip())
        commentamount=len(sel.xpath('//div[@class="exchange_thread_reply_rdr exchange-reply-container"]').extract())
        if commentamount > 0:
            for i in range(commentamount):
                item['commentContent'][response.url.strip()].append(''.join(sel.xpath('//div[@class="exchange_thread_reply_rdr exchange-reply-container"][{0}]/div[@class="thread_fmt"]/div[@class="post_fmt"]/text()|//div[@class="exchange_thread_reply_rdr exchange-reply-container"][{0}]/div[@class="thread_fmt"]/div[@class="post_fmt"]/a/text()|//div[@class="exchange_thread_reply_rdr exchange-reply-container"][{0}]/div[@class="thread_fmt"]/div[@class="post_fmt"]/ul/li/text()'.format(i+1)).extract()).strip())
                if len(sel.xpath('//div[@class="exchange_thread_reply_rdr exchange-reply-container"][{0}]/div[@class="thread_fmt"]/div[@class="post_hdr_fmt"]/a/@href'.format(i+1)).extract()) >0:
                    item['commentMaker'][response.url.strip()].append(sel.xpath('//div[@class="exchange_thread_reply_rdr exchange-reply-container"][{0}]/div[@class="thread_fmt"]/div[@class="post_hdr_fmt"]/a/@href'.format(i+1)).extract()[0])
                else:
                    item['commentMaker'][response.url.strip()].append('UnknownCommentMaker')
                
                #getCommentID
                commentIDList = sel.xpath('//a[@style="display:block"][{0}]/@id'.format(i+1)).extract()
                if len(commentIDList) >0:
                    item['commentID'][response.url.strip()].append(commentIDList[0])
                else:
                    item['commentID'][response.url.strip()].append('NoneID')
                
                if len(sel.xpath('//div[@class="exchange_thread_reply_rdr exchange-reply-container"][{0}]/div[@class="thread_fmt"]/div[@class="post_hdr_fmt"]/span[@class="mlResponseTo"]/a/@href'.format(i+1)).extract()) > 0:
                    item['commentReceiver'][response.url.strip()].append(sel.xpath('//div[@class="exchange_thread_reply_rdr exchange-reply-container"][{0}]/div[@class="thread_fmt"]/div[@class="post_hdr_fmt"]/span[@class="mlResponseTo"]/a/@href'.format(i+1)).extract()[0])
                else:
                    item['commentReceiver'][response.url.strip()].append(item['questionMaker'][response.url.strip()])
                
                if len(sel.xpath('//div[@class="exchange_thread_reply_rdr exchange-reply-container"][{0}]/div[@class="thread_fmt"]/div[@class="post_hdr_fmt"]/span[@class="mlResponseTo"]/a[2]/@href'.format(i+1)).extract()) >0:
                    item['commentRecvID'][response.url.strip()].append(sel.xpath('//div[@class="exchange_thread_reply_rdr exchange-reply-container"][{0}]/div[@class="thread_fmt"]/div[@class="post_hdr_fmt"]/span[@class="mlResponseTo"]/a[2]/@href'.format(i+1)).extract()[0].split('?pg')[1].split('#')[1])
                else:
                    item['commentRecvID'][response.url.strip()].append('Question')
                
                
                if len(sel.xpath('//div[@class="exchange_thread_reply_rdr exchange-reply-container"][{0}]/div[@class="thread_fmt"]/div[@class="posted_fmt"]/script/text()'.format(i+1)).extract())>0:
                    item['commentTime'][response.url.strip()].append(sel.xpath('//div[@class="exchange_thread_reply_rdr exchange-reply-container"][{0}]/div[@class="thread_fmt"]/div[@class="posted_fmt"]/script/text()'.format(i+1)).extract()[0])
                else:
                    item['commentTime'][response.url.strip()].append("UnknownCommentTime")
        #print [item['forumid'], item['questionTitle'], item['questionContent'], item['commentContent']]
        print [{"forumid":item['forumid']},{"questionTitle":item['questionTitle']},{"questionMaker":item['questionMaker']},{"questionTime":item['questionTime']},{"questionContent":item['questionContent']},{"commentID":item['commentID']},{"commentMaker":item['commentMaker']},{"commentReceiver":item['commentReceiver']},{"commentReceiveID":item['commentRecvID']},{"commentTime":item['commentTime']},{"commentContent":item['commentContent']}]
        return

            
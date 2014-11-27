# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class WebmdCodeItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class QCItem(Item):
    forumid = Field()
    questionTitle = Field()
    questionContent = Field()
    commentContent = Field()
    
    questionMaker = Field()
    commentMaker = Field()
    commentReceiver = Field()
    
    questionTime = Field()
    commentTime = Field()
    
    depth = Field()
    commentID = Field()
    
    commentRecvID = Field()
    
    pass
    

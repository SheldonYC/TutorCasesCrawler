# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class TutorscraperItem(scrapy.Item):
    source = scrapy.Field()
    case_id = scrapy.Field()
    subject = scrapy.Field()
    level = scrapy.Field()
    price = scrapy.Field()
    venue = scrapy.Field()
    remarks = scrapy.Field()

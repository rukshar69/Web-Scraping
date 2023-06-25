# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

#holds the extracted info.
class LuluScraperItem(scrapy.Item):
    # define the fields for your item here like:
    sub_cat = scrapy.Field() #subcategory of the electronic product
    item_url = scrapy.Field() #url of the product page
    item_name = scrapy.Field() # name of product
    item_price = scrapy.Field() #price of item
    item_summary = scrapy.Field() # dictionary object to hold summary points of the product

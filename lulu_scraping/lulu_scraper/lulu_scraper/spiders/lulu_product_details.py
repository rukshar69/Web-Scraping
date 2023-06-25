#STAGE 2: CRAWLING EACH PRODUCT'S SITE TO EXTRACT ITS NAME, PRICE, AND DESCRIPTION

import scrapy 
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from lulu_scraper.items import LuluScraperItem

#Command used in CMD: scrapy crawl lulu_prd -O products_desc.json
# The subcategory, product name, price, url and it's description are saved in a json file named products_desc.json

class LuluSpider(scrapy.Spider):
    name='lulu_prd' #name of spider crawler that's used in command line
    allowed_domains = ['luluhypermarket.com']
    start_urls = ['https://www.luluhypermarket.com/en-ae/electronics'] #the startpoint 

    def parse(self, response):
        #get the div cards that has the subcategory info such as link to subcategory product list
        for products in response.css('div.col-lg-2.col-md-2.col-auto'):
            item = LuluScraperItem()
            cat_link = products.css('a').attrib['href'] #get the partial link of product list of a particular sub category

            #https://www.luluhypermarket.com/c/HY00214796
            cat_link = 'https://www.luluhypermarket.com' + cat_link #construct absolute link to crawl into the site

            yield response.follow(cat_link, self.parse_category_page,meta={'item': item}) #crawl into the sub category item list page
    
    def parse_category_page(self, response): #method to get item list of a sub cat.
        
        for prd in response.css('div.product-box'): #access the div HTML card that contains link to product page
            
            item = response.meta['item']
            item['sub_cat'] = response.css('div.col-md h1.mb-1::text').get()
            #item['item_name'] = response.css('div.product-content div.product-desc h3::text').get().strip()
            item['item_url'] = prd.css('div.product-img a::attr(href)').get() #get product url
            item_link = 'https://www.luluhypermarket.com' +item['item_url'] #construct full product url
            yield response.follow(item_link, self.parse_individual_product_info,meta={'item': item}) #Go to the product page

    def parse_individual_product_info(self, response): #Method to extract product details from its respective page
        item = response.meta['item']

        #get item name and price
        item['item_name'] = response.css('div.product-description h1.product-name::text').get().strip()
        item['item_price'] = response.css('div.price-tag.detail span.current span.item.price span small::text').get().strip() + ' ' +response.css('div.price-tag.detail span.current span.item.price span::text').get().strip()
        
        #get item product summary
        #since the summary is a list of sentences we save the sentences in a dictionary
        product_summary_dict = {}
        # product_summary_dict[0] = response.css('div.description-block.mb-3.mt-md-0 h4::text').get()
        for i,d in enumerate(response.css('div.description-block.mb-3.mt-md-0 ul li::text')):
            product_summary_dict[i] = d.get()
        item['item_summary'] = product_summary_dict
        yield item # return the product details
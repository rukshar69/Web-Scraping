#STAGE 1: first stage to scrape all the listings for all sub cat. and the URLs of products

import scrapy 
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from lulu_scraper.items import LuluScraperItem

#Command used in CMD: scrapy crawl lulu -O products.csv
# The subcategory, product name and it's URL is saved in csv file named products.csv

class LuluSpider(scrapy.Spider):
    name='lulu' #name of spider crawler that's used in command line
    allowed_domains = ['luluhypermarket.com']
    start_urls = ['https://www.luluhypermarket.com/en-ae/electronics'] #the startpoint 

    def parse(self, response):
        #get the div cards that has the subcategory info such as link to subcategory product list
        for products in response.css('div.col-lg-2.col-md-2.col-auto'):
            cat_link = products.css('a').attrib['href'] #get the partial link of product list of a particular sub category

            #https://www.luluhypermarket.com/c/HY00214796
            cat_link = 'https://www.luluhypermarket.com' + cat_link #construct absolute link to crawl into the site

            yield response.follow(cat_link, self.parse_category_page,) #crawl into the sub category item list page
    
    def parse_category_page(self, response): #method to get item list of a sub cat.
        
        for prd in response.css('div.product-box'): #access the div HTML card that contains link to product page
            yield {
                'subcat': response.css('div.col-md h1.mb-1::text').get(),
                'prd_name': response.css('div.product-content div.product-desc h3::text').get().strip(), #get product name
                'prd_url': prd.css('div.product-img a::attr(href)').get() #get product url
            }
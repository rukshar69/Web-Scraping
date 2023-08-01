import pymongo

#sudo systemctl stop/start mongodb

class MongoDBPipeline:
    def __init__(self, mongo_uri, mongo_db, collection_name):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = collection_name

    @classmethod
    def from_crawler(cls, crawler):
        # Get the MongoDB settings from Scrapy settings
        mongo_uri = crawler.settings.get('MONGO_URI', 'mongodb://localhost:27017')
        mongo_db = crawler.settings.get('MONGO_DATABASE', 'scrapy_stocks')
        collection_name = crawler.settings.get('MONGO_COLLECTION', 'scrapy_stocks')  # Change 'scrapy_items' to your desired collection name
        return cls(mongo_uri, mongo_db, collection_name)

    def open_spider(self, spider):
        # Connect to the MongoDB database
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.collection_name]

    def close_spider(self, spider):
        # Close the MongoDB connection when the spider is closed
        self.client.close()

    def process_item(self, item, spider):
        # Insert the scraped item into the MongoDB collection
        self.collection.insert_one(dict(item))
        return item

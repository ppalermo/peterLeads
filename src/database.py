from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

class Database:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.websites = self.db.websites

    def save_website(self, website_data: dict) -> str:
        result = self.websites.insert_one(website_data)
        return str(result.inserted_id)

    def get_website(self, url: str) -> dict:
        return self.websites.find_one({'url': url})

    def update_website(self, url: str, data: dict) -> bool:
        result = self.websites.update_one(
            {'url': url},
            {'$set': data}
        )
        return result.modified_count > 0

    def get_all_websites(self):
        return list(self.websites.find()) 
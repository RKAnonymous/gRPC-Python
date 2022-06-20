import datetime
import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()
MONGODB_URI = os.environ["MONGODB_URI"]

client = MongoClient(MONGODB_URI)

mydb  = client.blog_database
collection = mydb.blog
# collection.delete_one({"_id": "1"})
# collection.delete_many({})
# for i in collection.find():
#     print(i)
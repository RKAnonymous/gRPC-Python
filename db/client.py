import datetime
import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()
MONGODB_URI = os.environ["MONGODB_URI"]

client = MongoClient(MONGODB_URI)

mydb = client["mydatabase"]
print(mydb.command("serverStatus"))

print(client.list_database_names())

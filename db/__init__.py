from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

uri = os.getenv("MONGODB_URI")
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.db_jungle
users_collection = db.users
articles_collection = db.articles

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

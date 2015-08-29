from pymongo import MongoClient
user_db_client = MongoClient("mongodb://localhost:27017")
activity_db_client = user_db_client
group_db_client = user_db_client
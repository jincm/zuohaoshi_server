from pymongo import MongoClient
import redis

from myapp import app

user_db_client = MongoClient(app.config['MONGODB_DATABASE'])#("mongodb://localhost:27017")
activity_db_client = user_db_client
group_db_client = user_db_client

redis_db = redis.Redis(app.config['REDIS_DB_HOST'], app.config['REDIS_DB_PORT'])
#activity_redis_client = user_redis_client
#group_redis_client = user_redis_client
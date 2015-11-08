from pymongo import MongoClient
import redis

from myapp import app

user_db_client = MongoClient(app.config['MONGODB_DATABASE'])  # ("mongodb://localhost:27017")
activity_db_client = user_db_client
group_db_client = user_db_client

# user_db_client.zuohaoshi.user_collection.create_index([('loc', "2d"), ('sex', 1)])

redis_db = redis.Redis(app.config['REDIS_DB_HOST'], app.config['REDIS_DB_PORT'])
# activity_redis_client = user_redis_client
# group_redis_client = user_redis_client

# init some values
CURRENT_USER_ID = 'current_user_id'


"""
import pymongo
from pymongo import MongoClient
con = MongoClient("mongodb://localhost:27017")

mydb = con.mydb # new a database
mydb.add_user('test', 'test') # add a user
mydb.authenticate('test', 'test') # check auth

muser = mydb.user # new a table

muser.save({'id':1, 'name':'test'}) # add a record

muser.insert({'id':2, 'name':'hello'}) # add a record
muser.find_one() # find a record

muser.find_one({'id':2}) # find a record by query

muser.create_index('id')

muser.find().sort('id', pymongo.ASCENDING) # DESCENDING
# muser.drop() delete table
muser.find({'id':1}).count() # get records number

muser.find({'id':1}).limit(3).skip(2) # start index is 2 limit 3 records

muser.remove({'id':1}) # delet records where id = 1

muser.update({'id':2}, {'$set':{'name':'haha'}}) # update one recor

"""
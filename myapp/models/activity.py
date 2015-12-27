# encoding: utf-8

"""
    zuohaoshi db
    Good man is well
"""
import time
import uuid

import json
from bson import ObjectId, json_util
import pymongo

from myapp.models import activity_db_client
from myapp.models.user import User
from myapp.models.group import Group
from myapp import app
from myapp.models import redis_db
from myapp.ext.face_match import FacePPSearch
activity_db = activity_db_client.zuohaoshi

# These keys are intentionally short, so as to save on memory in redis
POST_KEY = 'P'
PRAISE_NUM_FIELD = 'PN'
READ_NUM_FIELD = 'RN'

class Activity(object):
    def __init__(self, user_id=None, post_type="lost", post_id=None):
        app.logger.info("Activity instance:user_id:%s,%s,%s" % (user_id, post_type, post_id))
        self.user_id = user_id
        self.post_type = post_type  # update/group/activity/loster
        self.post_id = post_id
        self.participant = set()
        self.collection = activity_db.get_collection(post_type)

    @classmethod
    def post_activity(cls, user_id, post_type, post_data, post_id=None):
        app.logger.info("user:%s post one activity:%s, %s\n" % (user_id, post_type, post_data))
        one_activity = post_data
        # one_activity['user_id'] = user_id
        # one_activity['time'] = mytime
        # one_activity['img_urls'] = img_urls  # ["a.jpg","/b/c/d.jpg"]

        collection = activity_db.get_collection(post_type)
        if post_id is None:
            post_id = collection.insert_one(one_activity).inserted_id
            return {'post_id': str(post_id)}
        else:
            result = collection.update({'_id': ObjectId(post_id)}, {'$set': post_data})
            return dict({'post_id': str(post_id)}, **post_data)


    def get_one_activity(self):
        app.logger.info("get_activity %s,%s,%s" % (self.post_type, self.post_id, self.user_id))
        result = self.collection.find_one({'_id': ObjectId(self.post_id)})

        app.logger.info("get_activity result:%s" % result)
        if result is None:
            return {'Error': 'post not found'}

        # get other info from redis
        praise_num = redis_db.hget(POST_KEY + self.post_id, PRAISE_NUM_FIELD)
        praise_dict = {'praise_num': praise_num}

        ret = json.dumps(result, default=json_util.default)
        app.logger.info("get_activity %s" % ret)
        return json.loads(ret)

    def post_comment(self, comment_info):
        # check if the post's owner is current user
        app.logger.info("user:%s post one comment:%s, %s\n" % (self.user_id, self.post_type, self.post_id))
        app.logger.info("comment:%s\n", comment_info)

        praise = comment_info.get("praise")
        if praise:
            # dianzan, use redis hash, may record friends dianzan, other's only count
            redis_db.hincrby(POST_KEY + self.post_id, PRAISE_NUM_FIELD, praise)

        mycomment = comment_info.get('comment')
        if mycomment:
            new_info = dict()
            new_info['content'] = mycomment
            new_info['uid'] = self.user_id
            new_info['time'] = int(time.time())
            new_info['obj_id'] = ObjectId()
            resp = self.collection.update({'_id': ObjectId(self.post_id)}, {'$addToSet': {'comment': new_info}})
            return {'post_id': str(self.post_id), 'comment_id': str(new_info['obj_id'])}

        return {'post_id': str(self.post_id)}

    def del_comment(self, my_obj_id):
        # check if the post's owner is current user
        app.logger.info("user:%s del comment:%s, %s\n" % (self.user_id, self.post_id, uuid))
        info = dict()
        info['obj_id'] = ObjectId(my_obj_id)
        result = self.collection.update({'_id': ObjectId(self.post_id)}, {'$pull': {'comment': info}})

        return {'post_id': str(self.post_id)}

    def del_activity(self):
        app.logger.info("user:%s del activity:%s, %s\n" % (self.user_id, self.post_type, self.post_id))
        # check if the post's owner is current user
        res = self.collection.remove({'_id': ObjectId(self.post_id), 'uid': self.user_id})

        app.logger.info("del activity result:[%s]\n", res)

        # del redis db
        redis_db.hdel(POST_KEY + self.post_id, PRAISE_NUM_FIELD)

        return {'post_id': self.post_id}

    def get_sb_activity(self, user_id, limit, offset):
        app.logger.info("get_sb_activity of %s;limit:%d,%d\n", user_id, limit, offset)
        result = self.collection.find({'uid': user_id}).sort([("_id", -1)]).skip(offset).limit(limit)
        posts = []
        # if result has ObjectId type, then must change type as follow, otherwise will wrong
        # ret = json.dumps(result, default=json_util.default)
        # app.logger.info("show user %s" % ret)
        # return json.loads(ret)

        for loop in result:
            posts.append(loop)

        ret = dict()
        ret['posts'] = posts
        app.logger.info("get_sb_activity of %s;result:[%s]\n", user_id, ret)
        return ret

    def activity_search(self, args, fields, limit, offset):
        app.logger.info("person_nearby:[%s,%s,%s,%s]\n" % (args, fields, offset, limit))
        # result = self.collection.ensure_index({"loc": "2d", "_id": 1}, {"background": "true"})
        result = self.collection.ensure_index([("loc", pymongo.GEO2D), ("_id", 1)]) # ([("loc": "2d"), ("_id": 1)])
        condition = dict()
        loc = args.get('loc')
        if loc is None:
            find_result = self.collection.find().sort([("_id", -1)]).skip(offset).limit(limit)
        else:
            del args['loc']
            condition['loc'] = {'$near': loc}
            new_cond = dict(condition, **args)
            find_result = self.collection.find({'loc': {'$near': [11, 12]}}).skip(offset).limit(limit)

        # db.runCommand( { geoNear : "user_collection" , near : [50,50], num : 10 , query:{"age" : 233} });
        result = []
        # maybe only append some meta data, filter with fields
        for one in find_result:
            app.logger.info("activity find result [%s]\n" % one)
            result.append(one)

        app.logger.info("activity_search [%s]\n" % result)
        return {'posts': result}

    def lost_face_match(self, img1, img2):
        app.logger.info("lost_face_match:[%s,%s]\n" % (img1, img2))
        obj = FacePPSearch(app.logger, "lost", "beijing")
        ret = obj.face_match(img1, img2)
        return ret

    def track_activity(self, track):
        app.logger.info("user:%s post one comment:%s, %s\n" % (self.user_id, self.post_type, self.post_id))
        mytime = time.time()
        one_activity = {'track': track}
        post_id = self.collection.insert_one(one_activity).inserted_id

        return {'post_id': str(post_id)}

    def share_one_activity(self, share):
        return None


    def join_group_ask(self):
        pass
    def join_activity_ask(self):
        pass
    def join_group_confirm(self):
        pass
    def join_activity_confirm(self):
        pass

    def signout_group(self):
        pass
    def signout_activity(self):
        pass
    def del_from_group_byower(self):
        pass
    def del_from_activity_byower(self):
        pass

    def edit_group_info(self):
        pass



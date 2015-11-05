# encoding: utf-8

"""
    zuohaoshi db
    Good man is well
"""
import time
import uuid

import json
from bson import ObjectId, json_util

from myapp.models import activity_db_client
from myapp.models.user import User
from myapp.models.group import Group
from myapp import app
from myapp.models import redis_db

activity_db = activity_db_client.zuohaoshi

class Activity(object):
    def __init__(self, user_id=None, post_type=None, post_id=None):
        app.logger.info("Activity instance:user_id:%s,%s,%s" % (user_id, post_type, object_id))
        self.user_id = user_id
        self.post_type = post_type  # group/activity/loster
        self.post_id = post_id
        self.participant = set()
        self.collection = activity_db.get_collection(post_type)

    @classmethod
    def post_activity(cls, user_id, post_type, content, img_urls):
        app.logger.info("user:%s post one activity:%s, %s\n" % (user_id, post_type, content))
        mytime = int(time.time())
        one_activity = content
        one_activity['user_id'] = user_id
        one_activity['time'] = mytime
        one_activity['img_urls'] = img_urls  # ["a.jpg","/b/c/d.jpg"]

        collection = activity_db.get_collection(post_type)
        post_id = collection.insert_one(one_activity).inserted_id

        # save the post info to user db
        user = User(user_id)
        infos = dict()
        infos['post'] = '%s/%s' % (post_type, post_id)
        infos['lastud'] = mytime
        user.modify_user(infos, update='modify')

        return {'post_id': str(post_id)}

    def get_one_activity(self):
        app.logger.info("get_activity %s,%s,%s" % (self.post_type, self.post_id, self.user_id))
        result = self.collection.find_one({'_id': ObjectId(self.post_id)})
        ret = json.dumps(result, default=json_util.default)
        app.logger.info("get_activity %s" % ret)
        return json.loads(ret)

    def del_activity(self):
        app.logger.info("user:%s del activity:%s, %s\n" % (self.user_id, self.post_type, self.post_id))

        # check if the post's owner is current user
        res = self.collection.remove({'_id': self.post_id, 'user_id': self.user_id})

        info = dict()
        info['post'] = '%s/%s' % (self.post_type, self.post_id)
        # save the post info to user db
        user = User(self.user_id)
        user.modify_user(info, update='delete')

        return {'post_id': str(self.post_id)}

    def post_comment(self, comment):
        # check if the post's owner is current user
        app.logger.info("user:%s post one comment:%s, %s\n" % (self.user_id, self.post_type, self.post_id))
        app.logger.info("comment:%s\n", comment)

        praise = comment.get("praise")
        if praise == 1:
            # dianzan
            redis_db.incr(self.post_id)
        elif praise == -1:
            redis_db.decr(self.post_id)

        mycomment = comment.get('comment')
        if mycomment:
            new_info = dict()
            new_info['ct'] = mycomment
            new_info['user_id'] = self.user_id
            new_info['time'] = int(time.time())
            new_info['uuid'] = str(uuid.uuid4())
            resp = self.collection.update({'_id': self.post_id}, {'$addToSet': {'comment': new_info}})

        return {'post_id': str(self.post_id)}

    def del_comment(self, my_uuid):
        # check if the post's owner is current user
        app.logger.info("user:%s del comment:%s, %s\n" % (self.user_id, self.post_id, uuid))
        info = dict()
        info['uuid'] = my_uuid
        result = self.collection.update({'_id': self.post_id}, {'$pull': {'comment': info}})

        return {'post_id': str(self.post_id)}

    def track_activity(self, track):
        app.logger.info("user:%s post one comment:%s, %s\n" % (self.user_id, self.post_type, self.post_id))
        mytime = time.time()
        one_activity = {'track': track}
        post_id = self.collection.insert_one(one_activity).inserted_id

        return {'post_id': str(post_id)}

    def share_one_activity(self, share):
        return None

    def activity_search(self):
        pass




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



# encoding: utf-8

"""
    zuohaoshi db
    Good man is well
"""
import json
from bson import ObjectId, json_util

from myapp.models import activity_db_client
from myapp.models import user
from myapp import app

activity_db = activity_db_client.zuohaoshi
activity_collection = activity_db.activity_collecttion

class Activity(object):
    def __init__(self, object_id=None, user_id=None):
        self.object_id = object_id
        self.user_id = user_id
        #self.current_time = gettimeofday()
        self.participant = set()
        self.type = '' #group/activity/loster
        app.logger.info("Test for Activity db")

    def get_activity(self):
        app.logger.info("get_activity %s,%s" %(self.object_id, self.user_id))
        result = activity_collection.find_one({'_id': ObjectId(self.object_id)})
        ret = json.dumps(result, default=json_util.default)
        app.logger.info("get_activity %s" % ret)
        return json.loads(ret)

    @classmethod
    def post_activity(self, user_id, content):
        app.logger.info("user:%s post one activity:%s" % (user_id, content))
        one_activity = {'cotent': content, 'user_id': user_id}
        post_id = activity_collection.insert_one(one_activity).inserted_id

        return {'post_id': str(post_id)}

    def track_activity(self):
        pass
    def del_activity(self, user=None):
        pass

    def post_comment(self, user, content):
        pass
    def del_comment(self, user):
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

    def activity_nearby(self):
        pass

    def share_one_activity(self):
        pass



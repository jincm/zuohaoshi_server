# encoding: utf-8

"""
    zuohaoshi db
    Good man is well
"""
import json
from bson import ObjectId, json_util

from myapp.models import group_db_client
from myapp.models import user
from myapp import app

group_db = group_db_client.zuohaoshi
group_collection = group_db.group_collecttion

class Group(object):
    def __init__(self, object_id=None, user_id=None):
        app.logger.info("Group instance:%s,%s" % (object_id, user_id))
        self.object_id = object_id
        self.user_id = user_id

    def get_one_group(self):
        app.logger.info("get_activity %s,%s" %(self.object_id, self.user_id))
        result = group_collection.find_one({'_id': ObjectId(self.object_id)})
        ret = json.dumps(result, default=json_util.default)
        app.logger.info("get_activity %s" % ret)
        return json.loads(ret)

    @classmethod
    def post_group(cls, user_id, group):
        app.logger.info("user:%s post one activity:%s" % (user_id, group))
        one_group = {'group': group, 'user_id': user_id}
        group_id = group_collection.insert_one(one_group).inserted_id

        return {'group_id': str(group_id)}

    def track_group(self):
        pass
    def del_group(self, user=None):
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

    def group_nearby(self):
        pass

    def group_search(self):
        pass

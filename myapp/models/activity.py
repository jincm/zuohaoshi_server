# encoding: utf-8

"""
    zuohaoshi db
    Good man is well
"""

from myapp.models import client

from myapp import app

activity_db = client.zuohaoshi


class Activity(object):
    def __init__(self, object_id=0, operator=''):
        self.object_id = object_id
        #self.owner = ''
        self.operator = operator
        self.current_time = gettimeofday()
        self.participant = set()
        self.type = '' #group/activity/loster
        app.logger.info("Test for Activity db")
        pass

    def get_activity(self):
        pass
    def post_activity(self):
        pass
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



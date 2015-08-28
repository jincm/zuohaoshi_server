# encoding: utf-8

"""
    zuohaoshi db
    Good man is well
"""

from myapp.models import client

from myapp import app

group_db = client.zuohaoshi

class Group(object):
    def __init__(self):
        app.logger.info("Test for Group db")
        pass
    def get_group(self):
        pass
    def post_group(self):
        pass
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

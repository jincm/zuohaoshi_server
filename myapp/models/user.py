# encoding: utf-8

"""
    zuohaoshi db
    Good man is well
"""
import random

from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from myapp.models import client
from bson.objectid import ObjectId

from myapp import app

user_db = client.zuohaoshi

class User(object):

    def __init__(self, user_id=None):
        app.logger.info("Test for user db")
        self.user_id = user_id
        self.phone = None

        self.friends = set()
        self.feeds = set()
        self.followers = set()
        self.type = 0 #user/shangjia/qiye/aixinshe/jijinhui
        self.id = 0
        self.head_pic = ''
        self.notes = ''

    def __repr__(self):
        return '<User %r>' % (self.user_id)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=0):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

    def get_user(self):
        app.logger.info("Test for get user\n")
        pass
    def add_user(self):
        pass
    def del_user(self):
        pass
    def edit_user_info(self):
        pass
    def follow_sb(self):
        pass
    def unfollow_sb(self):
        pass
    def add_friend_ask(self):
        pass
    def add_friend_confirm(self):
        pass
    def person_nearby(self):
        pass
    def search_one_person(self):
        pass

    def login(self):
        pass
    def logout(self):
        pass

    def register_user(self, phonenum=0, identify_code=None, passwd=None):
        if identify_code is None:
            identify_code = random.randint(111111, 999999)
            #save to redis

            #call API send identify_code to phonenum
            msg = u"[做好事]: %d ,请与10分钟内完成手机号验证操作"
            #log(phonenum,msg)
        else:
            #get identify_code from redis check phonenum
            self.add_user(phonenum,passwd)




def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = Haoshi_User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = Haoshi_User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True




class Loster(object):
    def __init__(self):
        pass


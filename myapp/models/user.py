# encoding: utf-8

"""
    zuohaoshi db
    Good man is well
"""
import random
import os
import sys
import datetime
import json
from bson import ObjectId, json_util

from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from myapp.models import user_db_client
from myapp import app

user_db = user_db_client.zuohaoshi
user_collection = user_db.user_collection

class User(object):

    def __init__(self, user_id=None):
        app.logger.info("user instance %s init" % user_id)
        self.user_id = user_id
        #self.id = user_id

        self.phone = None
        self.friends = set()
        self.feeds = set()
        self.followers = set()
        self.type = 0 #user/shangjia/qiye/aixinshe/jijinhui
        self.head_pic = ''
        self.notes = ''

    def __repr__(self):
        return '<User %r>' % (self.user_id)

    def is_authenticated(self):
        app.logger.info("authenticated")
        return True

    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        """
        Assuming that the user object has an `id` attribute, this will take
        that and convert it to `unicode`.
        """
        try:
            return (self.user_id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override get_id")

    def show_user(self):
        app.logger.info("show user %s" % self.user_id)
        result = user_collection.find_one({'_id': ObjectId(self.user_id)})
        ret = json.dumps(result, default=json_util.default)
        app.logger.info("show user %s" % ret)
        return json.loads(ret)

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

    def logout(self):
        app.logger.info("Login failed:[%s]" % self.user_id)
        #clear redis token
        return {'logout': self.user_id}

    @classmethod
    def get_user_fromtoken(self, token):
        app.logger.info("get user from token:%s\n" % token)
        #get accout from redis according token
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token

        user_id = data['object_id']
        user = User(user_id)
        app.logger.info("get user from token:%s %s\n" % (token, user.user_id))
        return user

    @classmethod
    def login(self, accout=None, passwd=None):
        app.logger.info("Login start:[%s]" % accout)
        #get passwd hash/object_id from mongodb
        result_find = user_collection.find_one({'accout': accout})
        db_passwd_hash = result_find['passwd_hash']
        object_id = result_find['_id']

        try:
            ret = pwd_context.verify(passwd, db_passwd_hash)
            if not ret:
                app.logger.info("Login failed:[%s]" % accout)
                return {'error': 'login failed'}
        except:
            app.logger.info("Login failed:[%s]" % accout)
            return {'error': 'login failed'}
        else:
            #generate token
            s = Serializer(app.config['SECRET_KEY'], expires_in=6000)#3600000=41 day
            token = s.dumps({'object_id': '%s' % object_id, 'password': passwd})
            #save token to redis

            app.logger.info("Login success:[%s:%s:%s]" % (accout, object_id, token))
            return {"login": accout, "token": token}


    @classmethod
    def add_user(self, accout=None, passwd=None):
        app.logger.info("add user start:[%s,%s]" % (accout, passwd))
        #generate token
        s = Serializer(app.config['SECRET_KEY'], expires_in=6000)
        object_id = 'test'
        token = s.dumps({'object_id': '%s' % object_id, 'password': passwd})
        #save token to redis

        #save accout/passwd to mongodb
        passwd_hash = pwd_context.encrypt(passwd)
        one_user = {'accout': accout, 'passwd_hash': passwd_hash}
        user_obj_id = user_db.user_collection.insert_one(one_user).inserted_id

        app.logger.info("add user [%s:%s:%s:%s]" % (accout, passwd_hash, token, user_obj_id))
        return token, user_obj_id

    @classmethod
    def register_user(self, accout=None, identify_code=None, passwd=None):
        #username may be phone_num or email
        if identify_code is None:
            identify_code = random.randint(111111, 999999)
            #call API send identify_code to phonenum
            if len(accout) == 11:#from app/web/weixin
                msg = u"[做好事]: %d ,请与10分钟内完成手机号验证操作"
            app.logger.info("Get identify_code:%s for user %s" % (str(identify_code), accout))
            #set it to redis {accout:identify_code}

            return {'identify_code': identify_code}
        else:
            #get identify_code from redis {accout:identify_code}
            saved_identify_code = '111111'
            if identify_code == saved_identify_code:
                #delete identify_code from redis {accout:identify_code}

                app.logger.info("Identify success for accout %s" % accout)
                token, user_obj_id = self.add_user(accout, passwd)
                return {"register": accout, "token": token}
            else:
                app.logger.info("Identify error:%s,code:%s,saved:%s" % (accout, identify_code, saved_identify_code))
                return {'error': 'Identify code not match'}


class Loster(object):
    def __init__(self):
        pass


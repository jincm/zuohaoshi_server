# encoding: utf-8

"""
    zuohaoshi db
    Good man is well
"""
import random
import os
import sys
import datetime

from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from myapp.models import user_db_client
from bson.objectid import ObjectId

from myapp import app

user_db = user_db_client.zuohaoshi


class User(object):

    def __init__(self, user_id=None):
        app.logger.info("user instance %s init" % user_id)
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
    def is_authenticated(self):
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
            return unicode(self.id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override get_id")

    def show_user(self):
        app.logger.info("show user %s" % self.user_id)
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

    def logout(self):
        app.logger.info("Login failed:[%s]" % self.user_id)
        #clear redis token

    @classmethod
    def get_user_fromtoken(self, token):
        app.logger.info("get user from token:%s\n" % token)
        #get accout from redis according token
        token = 'caicaiwoshishui'
        user_id = '123456'
        user = User(user_id)
        return user

    @classmethod
    def login(self, accout=None, passwd=None):
        #passwd_hash = self.hash_password(passwd)
        app.logger.info("save to mongodb [%s:%s]" % (accout, passwd_hash))
        #get passwd_hash from mongodb
        db_passwd = "passwdisone"
        ret = pwd_context.verify(passwd, db_passwd)
        if db_passwd == '':
            app.logger.info("Login success:[%s]" % accout)
            return "Login success"
        else:
            app.logger.info("Login failed:[%s]" % accout)
            return "Login failed"

    @classmethod
    def add_user(self, accout=None, passwd=None):
        app.logger.info("add user:[%s,%s]" % (accout, passwd))
        #generate token
        s = Serializer(app.config['SECRET_KEY'], expires_in=0)
        token = s.dumps({'id': 0})
        token = "caicaiwoshishui"
        #save token to redis

        #save accout/passwd to mongodb
        passwd_hash = pwd_context.encrypt(passwd)
        app.logger.info("save to mongodb [%s:%s]" % (accout, passwd_hash))

    @classmethod
    def register_user(self, accout=None, identify_code=None, passwd=None):
        #username may be phone_num or email
        if identify_code is None:
            identify_code = random.randint(111111, 999999)
            #call API send identify_code to phonenum
            if len(accout) == 11:#from app/web/weixin
                msg = u"[做好事]: %d ,请与10分钟内完成手机号验证操作"
            app.logger.info("Get identify_code:%s for user %s" %(str(identify_code), accout))
            #set it to redis

            return {'identify_code':identify_code}
        else:
            #get identify_code from redis to check username and its identify code
            saved_identify_code = '111111'
            if identify_code == saved_identify_code:
                app.logger.info("Identify success for accout %s" % accout)
                ret = self.add_user(accout, passwd)
                return {"accout": accout}
            else:
                app.logger.info("Identify error for user:%s,code:%s" % (accout, identify_code))
                #return "Error"
                abort(400)




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


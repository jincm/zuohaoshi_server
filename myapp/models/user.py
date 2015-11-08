# encoding: utf-8

"""
    zuohaoshi db
    Good man is well
"""
import random
import time
import os
import sys
import datetime
import json
from bson import ObjectId, json_util

from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

import pymongo

from myapp.models import user_db_client
from myapp.models import redis_db, CURRENT_USER_ID
from myapp.ext.short_message import send_short_message
from myapp.ext.easemob import EasemobIM
from myapp import app

user_db = user_db_client.zuohaoshi
user_collection = user_db.user_collection
# user_db.user_collection.create_index("_id")

if redis_db.get(CURRENT_USER_ID) is None:
    redis_db.set(CURRENT_USER_ID, '10000')

im_obj = EasemobIM(app.logger)

# These keys are intentionally short, so as to save on memory in redis
FRIENDS_KEY = 'FR'
FOLLOWS_KEY = 'F'
FOLLOWERS_KEY = 'f'
BLOCKS_KEY = 'B'
BLOCKED_KEY = 'b'

USERID_KEY = 'U'

class User(object):

    def __init__(self, user_id=None):
        app.logger.info("user instance %s init" % user_id)
        self.user_id = user_id

        """
        self.score = 0
        self.phone = None
        self.friends = set()
        self.feeds = set()
        self.followers = set()
        self.type = 0  # user/shangjia/qiye/aixinshe/jijinhui
        self.head_pic = ''
        self.notes = ''
        """

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
            return self.user_id
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override get_id")

    def show_user(self):
        app.logger.info("show user %s" % self.user_id)
        result = user_collection.find_one({'_id': self.user_id})  # ObjectId(self.user_id)})
        if result:
            try:
                del result['passwd_hash']
            except Exception, e:
                app.logger.error("del key passwd_hash error:%s", e)

        # app.logger.info("show user %s" % result)
        # if result has ObjectId type, then must change type as follow, otherwise will wrong
        # ret = json.dumps(result, default=json_util.default)
        # app.logger.info("show user %s" % ret)
        # return json.loads(ret)
        return result

    @classmethod
    def get_user_from_token(cls, token):
        app.logger.info("get user from token:%s\n" % token)
        # get account from redis according token
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        except:
            return None

        user_id = data['user_id']
        user = User(user_id)

        # users last online time, may be update redis not mongodb
        mytime = int(time.time())
        infos = dict()
        infos['last_update'] = mytime
        user.modify_user(infos, update='modify')

        app.logger.info("get user from token:%s %s\n" % (token, user.user_id))
        return user

    @classmethod
    def add_user(cls, account=None, passwd=None):
        app.logger.info("add user start:[%s,%s]" % (account, passwd))
        # check if account has register
        result_find = user_collection.find_one({'account': account})
        if result_find:
            db_passwd_hash = result_find.get('passwd_hash')
            user_id = result_find.get('_id')
            s = Serializer(app.config['SECRET_KEY'], expires_in=6000)  # 3600000=41 days
            token = s.dumps({'user_id': '%s' % user_id, 'passwd': db_passwd_hash})
            app.logger.info("user exsit [account:%s]:[user_id:%s]:[%s]\n" % (account, user_id, token))
            return token, str(user_id)

        # generate token
        user_id = str(redis_db.incr(CURRENT_USER_ID))
        s = Serializer(app.config['SECRET_KEY'], expires_in=6000)  # 3600000=41 days
        token = s.dumps({'user_id': '%s' % user_id, 'passwd': passwd})

        # save account/passwd to mongodb
        passwd_hash = pwd_context.encrypt(passwd)
        one_user = {'_id': user_id, 'account': account, 'passwd_hash': passwd_hash}
        # user_obj_id = user_db.user_collection.insert_one(one_user).inserted_id
        user_obj_id = user_db.user_collection.insert_one(one_user).inserted_id

        # save token to redis
        redis_db.set(str(user_id), token)
        # save user to easemob platform
        im_obj.register_user(user_id, user_id)

        app.logger.info("add user [%s]:[%s]:[%s]:%s]" % (account, passwd_hash, token, user_id))
        return token, str(user_id)

    @classmethod
    def register_user(cls, account=None, identify_code=None, passwd=None):
        # username may be phone_num or email
        if identify_code is None:
            identify_code = random.randint(111111, 999999)
            # call API send identify_code to phone num
            if len(account) == 11:  # from app/web/weixin
                msg = u"[做好事]: %d ,请与10分钟内完成手机号验证操作" % identify_code
                send_short_message(account, msg)
            app.logger.info("Get identify_code:%s for user %s" % (str(identify_code), account))

            # set it to redis {account:identify_code} and set expire time
            redis_db.set(account, identify_code)
            redis_db.expire(account, 600)

            return {'identify_code': str(identify_code)}
        else:
            # get identify_code from redis {account:identify_code}
            saved_identify_code = redis_db.get(account)

            if identify_code == saved_identify_code:
                # delete identify_code from redis {account:identify_code}
                redis_db.delete(account)

                app.logger.info("Identify success for account %s" % account)
                token, user_obj_id = cls.add_user(account, passwd)
                return {"account": account, "token": token, "user_id": user_obj_id}
            else:
                app.logger.info("Identify error:%s,code:%s,saved:%s" % (account, identify_code, saved_identify_code))
                return {'error': 'Identify code not match'}

    def del_user(self, user_id):
        app.logger.info("del_user start:[%s]" % (user_id))

        # delete head portrait from store

        # delete from db
        # user_obj_id = user_db.user_collection.remove(one_user).inserted_id

        # clear redis token
        redis_db.delete(self.user_id)

        # delete his activities in db

        app.logger.info("del_user [%s:%s]" % (self.user_id, user_id))
        return {'del': user_id}

    @classmethod
    def login(cls, account=None, passwd=None):
        app.logger.info("Login start:[%s]" % account)
        # get password hash/object_id from mongodb
        result_find = user_collection.find_one({'account': account})
        db_passwd_hash = result_find['passwd_hash']
        object_id = result_find['_id']

        try:
            ret = pwd_context.verify(passwd, db_passwd_hash)
            if not ret:
                app.logger.info("Login failed:[%s]" % account)
                return {'error': 'login failed'}
        except Exception, e:
            app.logger.error("Login failed:[%s]" % account)
            app.logger.error(e)
            return {'error': 'login failed'}
        else:
            # generate token
            s = Serializer(app.config['SECRET_KEY'], expires_in=6000)  # 3600000=41 days
            token = s.dumps({'user_id': '%s' % object_id, 'passwd': passwd})
            # save token to redis
            redis_db.set(str(object_id), token)

            app.logger.info("Login success:[%s:%s:%s]" % (account, object_id, token))
            return {"login": account, "token": token, "user_id": str(object_id)}

    def logout(self):
            app.logger.info("Login failed:[%s]" % self.user_id)
            # clear redis token
            redis_db.delete(self.user_id)

            return {'logout': self.user_id}

    def modify_user(self, info, update='modify'):
        app.logger.info("save user's new info to db:[%s]" % info)
        if update == 'modify':
            """
            for one in info:
                new_info = {one: info[one]}
                if one in ['post', 'friends', 'follower', 'followee']:
                    # result = user_db.user_collection.update({'_id': self.user_id}, {'$addToSet': info})
                    result = user_db.user_collection.update({'_id': self.user_id}, {'$push': new_info})
            """
            token = info.get("token")
            if token:
                try:
                    del info["token"]
                except Exception, e:
                    app.logger.error("del key error:%s", e)

            result = user_db.user_collection.update({'_id': self.user_id}, {'$set': info})
        elif update == 'delete':
            new_info = info
            result = user_db.user_collection.update({'_id': self.user_id}, {'$pull': new_info})

        if result.get('ok') != 1:
            app.logger.error("result is %s" % result)
            return result

        app.logger.info("modify_user [%s:%s]" % (self.user_id, result))
        return {'modifyok': self.user_id}

    @classmethod
    def users_search(cls, args, fields, offset, limit):
        app.logger.info("person_nearby:[%s,%s,%s,%s]\n" % (args, fields, offset, limit))
        # may be first create index
        result = user_db.user_collection.ensure_index([("loc", pymongo.GEO2D), ("sex", 1)])

        condition = dict()
        loc_x = int(args.get('loc_x'))
        loc_y = int(args.get('loc_y'))
        loc = []
        loc.append(loc_x)
        loc.append(loc_y)
        app.logger.info("loc:[%s]\n" % loc)
        if loc is None:
            find_result = user_db.user_collection.find(args).skip(offset).limit(limit)
        else:
            # del args['loc']
            condition['loc'] = {'$near': loc}
            new_cond = dict(condition, **args)
            find_result = user_db.user_collection.find(condition).skip(offset).limit(limit)

        # db.runCommand( { geoNear : "user_collection" , near : [50,50], num : 10 , query:{"age" : 233} });
        result = []
        # maybe only append some meta data, filter with fields
        for one in find_result:
            app.logger.info("users find result [%s]\n" % one)
            if 'passwd_hash' in one:
                del one['passwd_hash']
            result.append(one)

        app.logger.info("users_search [%s]\n" % result)
        return {'users': result}

    def add_friend_ask(self, friend_id, msg=None):
        app.logger.info("add_friend_ask:[%s]" % friend_id)

        ask_user = self.show_user()
        self.follow_sb(self.user_id, friend_id)

        # send ask info to him
        msg_body = {}
        msg_body['target_type'] = "users"
        msg_body['target'] = [friend_id]
        msg_body['msg'] = {"type": "txt", "msg": '%s' % msg}
        msg_body['from'] = self.user_id

        im_obj.send_txt_msg(self.user_id, msg_body)

        app.logger.info("add_friend_ask [%s:%s]" % (self.user_id, msg))
        return {'add_friend_ask_ok': self.user_id}

    def add_friend_confirm(self, friend_id):
        app.logger.info("add_friend_confirm:[%s]" % friend_id)

        confirm_user = self.show_user()

        # add follow on redis
        self.follow_sb(self.user_id, friend_id)

        # add friend on redis
        self.add_friend(self.user_id, friend_id)

        # add friend on IM platform
        im_obj.add_friend(self.user_id, friend_id)

        app.logger.info("add_friend_confirm [%s]" % self.user_id)
        return {'add_friend_ok': self.user_id}

    def add_friend(self, from_user, to_user):
        forward_key = '%s:%s' % (FRIENDS_KEY, from_user)
        ret = redis_db.sadd(forward_key, to_user)

        app.logger.info("follow:[%s],[%s],[ret:%s]" % (from_user, to_user, ret))
        return ret

    def del_friend(self, from_user, to_user):
        forward_key = '%s:%s' % (FRIENDS_KEY, from_user)
        ret = redis_db.srem(forward_key, to_user)

        app.logger.info("un_follow:[%s],[%s],[ret:%s]" % (from_user, to_user, ret))
        return ret

    def follow_sb(self, from_user, to_user):
        forward_key = '%s:%s' % (FOLLOWS_KEY, from_user)
        forward = redis_db.sadd(forward_key, to_user)
        reverse_key = '%s:%s' % (FOLLOWERS_KEY, to_user)
        reverse = redis_db.sadd(reverse_key, from_user)

        ret = forward and reverse
        app.logger.info("follow:[%s],[%s],[ret:%s]" % (from_user, to_user, ret))
        return ret

    def un_follow_sb(self, from_user, to_user):
        forward_key = '%s:%s' % (FOLLOWS_KEY, from_user)
        forward = redis_db.srem(forward_key, to_user)
        reverse_key = '%s:%s' % (FOLLOWERS_KEY, to_user)
        reverse = redis_db.srem(reverse_key, from_user)
        ret = forward and reverse
        app.logger.info("un_follow:[%s],[%s],[ret:%s]" % (from_user, to_user, ret))
        return ret

    def block(self, from_user, to_user):
        forward_key = '%s:%s' % (BLOCKS_KEY, from_user)
        forward = redis_db.sadd(forward_key, to_user)
        reverse_key = '%s:%s' % (BLOCKED_KEY, to_user)
        reverse = redis_db.sadd(reverse_key, from_user)
        ret = forward and reverse
        app.logger.info("block:[%s],[%s],[ret:%s]" % (from_user, to_user, ret))
        return ret

    def unblock(self, from_user, to_user):
        forward_key = '%s:%s' % (BLOCKS_KEY, from_user)
        forward = redis_db.srem(forward_key, to_user)
        reverse_key = '%s:%s' % (BLOCKED_KEY, to_user)
        reverse = redis_db.srem(reverse_key, from_user)
        ret = forward and reverse
        app.logger.info("unblock:[%s],[%s],[ret:%s]" % (from_user, to_user, ret))
        return ret

    def get_follows(self, user):
        follows = redis_db.smembers('%s:%s' % (FOLLOWS_KEY, user))
        blocked = redis_db.smembers('%s:%s' % (BLOCKED_KEY, user))

        ret = list(follows.difference(blocked))
        app.logger.info("get_follows:[%s],[ret:%s]" % (user, ret))
        return ret

    def get_followers(self, user):
        followers = redis_db.smembers('%s:%s' % (FOLLOWERS_KEY, user))
        blocks = redis_db.smembers('%s:%s' % (BLOCKS_KEY, user))
        ret = list(followers.difference(blocks))
        app.logger.info("get_followers:[%s],[ret:%s]" % (user, ret))
        return ret

    def get_blocks(self, user):
        return list(redis_db.smembers('%s:%s' % (BLOCKS_KEY, user)))

    def get_blocked(self, user):
        return list(redis_db.smembers('%s:%s' % (BLOCKED_KEY, user)))

    def get_friends(self, user):
        return list(redis_db.smembers('%s:%s' % (FRIENDS_KEY, user)))

    def search_one_person(self):
        pass

    def get_sb_activities(self):
        index = 10
        num = 10
        return ""  # should use show_user


class Loster(object):
    def __init__(self):
        pass


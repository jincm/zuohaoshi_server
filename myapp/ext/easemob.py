# encoding: utf-8

"""
    zuohaoshi admin
    Be a good man
    封装了环信的接口
"""
from time import time
import os
import sys
import string
import random
import json

import requests

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from myapp.models import redis_db


#Instant Messaging base class
class ImBase(object):
    def register_user(self, username, passwd, nickname=None):
        pass

    def register_users(self, userslist):
        pass

    def get_user(self, username):
        pass

    def get_users(self, limit,cursor=None):
        pass

    def del_user(self, username):
        pass

    def reset_passwd(self, username, passwd):
        pass

    def change_nickname(self, username, nickname):
        pass

    def add_friend(self, username, friend_username):
        pass

    def del_friend(self, username, friend_username):
        pass

    def get_friends(self, username):
        pass

    def get_blacklists(self, username):
        pass

    def blacklist_one(self, username, blacklist_users):
        pass

    def unblacklist_one(self, username, blacklist_user):
        pass

    def check_online(self, username):
        pass

    def offline_msg_count(self, username):
        pass

    def offline_msg_status(self, username, msg_id):
        pass

    def deactivate_user(self, username):
        pass

    def activate_user(self, username):
        pass

    def disconnect_user(self, username):
        pass

    def upload_file(self, username, file):
        pass

    def download_file(self, username, file_uuid):
        pass

    def send_txt_msg(self, username, msg_body):
        pass

    def send_img_msg(self, username, msg_body):
        pass

    def send_audio_msg(self, username, msg_body):
        pass

    def send_video_msg(self, username, msg_body):
        pass

    def send_cmd_msg(self, username, msg_body):
        pass

    def get_chatgroups(self, username):
        pass

    def get_chatgroups_bypages(self, username):
        pass

    def get_group_detail(self, username, group_ids):
        pass

    def create_chatgroup(self, username, group_body):
        pass

    def change_chatgroup(self, username, group_body):
        pass

    def del_chatgroup(self, group_id):
        pass

    def getusers_in_chatgroup(self, group_id):
        pass

    def add_member_to_chatgroup(self, username, group_id, new_user):
        pass

    def add_members_to_chatgroup(self, username, group_id, new_users):
        pass

    def del_member_from_chatgroup(self, username, group_id, del_user):
        pass

    def del_members_from_chatgroup(self, username, group_id, del_users):
        pass

    def get_userjoined_chatgroups(self, username):
        pass

    def change_chatgroup_owner(self, username, newowner):
        pass

    def getblacklist_of_chatgroup(self, group_id):
        pass

    def addblacklist_to_chatgroup(self, username, group_id, black_user):
        pass

    def addblacklists_to_chatgroup(self, username, group_id, black_users):
        pass

    def delblacklist_from_chatgroup(self, username, group_id, black_user):
        pass

    def delblacklists_from_chatgroup(self, username, group_id, black_users):
        pass

    def create_chatroom(self, username, chatroom_body):
        pass

    def change_chatroom(self, username, chatroom_id, chatroom_body):
        pass

    def del_chatroom(self, username, chatroom_id):
        pass

    def get_all_chatrooms(self, ):
        pass

    def get_one_chatroom(self, chatroom_id):
        pass

    def get_userjoined_chatrooms(self, username):
        pass

    def adduser_to_chatroom(self, username, chatroomid):
        pass

    def addusers_to_chatroom(self, userslist, chatroomid):
        pass

    def deluser_from_chatroom(self, username, chatroomid):
        pass

    def deluser_from_chatroom(self, userslist, chatroomid):
        pass


##################################################################################
#**************************easemob************************************************
##################################################################################

##################################################################################
#######################token######################################################
##################################################################################
endpoint = "https://a1.easemob.com"
appurl = "/xinsongkeiji/zuohaoshi"

client_id = "YXA6a-DesDq8EeWK3s2W6XnvYw"
client_secret = "YXA6QqxIMUblL2RxyObKWlykfvHqItA"

JSON_HEADER = {'content-type': 'application/json'}
EASEMOB_TOKEN_KEY = "easemob_token"
##################################################################################
#######################User#######################################################
##################################################################################

"""
在注册环信账户的时候， 需要注意环信ID的规则：

环信ID需要使用英文字母和（或）数字的组合
环信ID不能使用中文
环信ID不能使用email地址
环信ID不能使用UUID
环信ID中间不能有空格或者井号（#）等特殊字符
允许的用户名正则 “[a-zA-Z0-9_-.]*” (a~z大小写字母/数字/横线/下划线/英文点) 其他都不允许
环信ID不区分大小写。系统忽略大小写，认为AA,Aa,aa,aA都是一样的,如果系统已经存在了环信ID为AA的用户，
再试图使用aa作为环信ID注册新用户，系统返回用户名重复,以此类推。但是请注意：环信ID在数据上的表现形
式还是用户最初注册的形式，注册时候使用的大写就保存大写，是小写就保存小写，即:使用AA注册，环信保存
的ID就是AA;使用Aa注册，环信保存的ID就是Aa,以此类推。
"""


class EasemobIM(ImBase):
    def __init__(self, mylogger):
        self.logger = mylogger
        self.logger.info("easemob_IM init\n")

    def easemob_request(self, url, method, payload=None, headers=JSON_HEADER, auth=None):
        try:
            if auth:
                headers['Authorization'] = 'Bearer ' + auth

            self.logger.info("%s %s:data[%s] head:%s\n", method, url, payload, headers)

            if method == 'GET':
                r = requests.get(url, headers=headers)
            elif method == 'POST':
                r = requests.post(url, data=json.dumps(payload), headers=headers)
            elif method == 'DELETE':
                r = requests.delete(url, headers=headers)
            else:
                self.logger.info("request no method\n")
                return True
        except Exception, e:
            print "error is coming......................."
            print e
            self.logger.error("error is coming..........:%s\n" % e)

            return False, e
        finally:
            if r.status_code == requests.codes.ok:
                return True, r.json()
            else:
                print "error is coming......................."
                return False, r.text

    #Request Headers : {“Content-Type”:”application/json”}
    #POST /{org}/{app}/token {'grant_type':'client_credentials', 'client_id':'xxxx', 'client_secret':'xxxxx'}
    #curl -X POST "https://a1.easemob.com/xinsongkeiji/zuohaoshi/token" -d '{"grant_type":"client_credentials","client_id":"YXA6a-DesDq8EeWK3s2W6XnvYw","client_secret":"YXA6QqxIMUblL2RxyObKWlykfvHqItA"}'
    #{"access_token":"YWMtRVd2Ym-7EeWShyclC9OgCwAAAVGJmnx_I0zX-i46BMevXC5vvXeBGMoY1qU","expires_in":5184000,"application":"6be0deb0-3abc-11e5-8ade-cd96e979ef63"}
    def easemob_get_token(self):
        token_get = redis_db.get(EASEMOB_TOKEN_KEY)
        token = None
        if token_get is not None:
            self.logger.info("Get token from redis " + token_get)
            token, expires = token_get.split("+")

        if token is None or time() > expires:
            url = endpoint + appurl + "/token"
            payload = {'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': client_secret}

            success, result = self.easemob_request(url, "POST", payload)
            self.logger.info("Get token from " + url + "\n" + result['access_token'])
            #save token to redis
            token = result['access_token']
            token_new = result['access_token'] + "+" + str(result['expires_in'] + int(time()))
            redis_db.set(EASEMOB_TOKEN_KEY, token_new)

        return token

    """
    授权注册
    Path : /{org_name}/{app_name}/users
    HTTP Method : POST
    URL Params ： 无
    Request Headers : {“Content-Type”:”application/json”,”Authorization”:”Bearer ${token}”}
    Request Body ： {“username”:”${用户名}”,”password”:”${密码}”, “nickname”:”${昵称值}”}
    """
    def register_user(self, username, passwd, nickname=None):
        token = self.easemob_get_token()
        url = endpoint + appurl + "/users"
        payload = {'username': username, 'password': passwd, 'nickname': nickname}

        success, result = self.easemob_request(url, "POST", payload, auth=token)
        self.logger.info("register_user reulst is %s " % result)

        return result
    """
    注册IM用户[批量]
    Path : /{org_name}/{app_name}/users
    HTTP Method : POST
    URL Params ： 无
    Request Headers : {“Content-Type”:”application/json”,”Authorization”:”Bearer ${token}”}
    Request Body ： [{“username”:”${用户名1}”,”password”:”${密码}”},…,{“username”:”${用户名2}”,”password”:”${密码}”}]
    """
    def register_users(self, userslist):
        pass

    """
    Path : /{org_name}/{app_name}/users/{username}
    HTTP Method : GET
    URL Params ：无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ： 无
    Response Body ： 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略。
    可能的错误码：
    404 （用户不存在） 401（未授权[无token,token错误,token过期]） 5xx 详见 服务器端REST API常见错误码
    """
    def get_user(self, username):
        pass

    """
    该接口默认返回最早创建的10个用户，如果需要指定获取数量，需加上参数limit=N，N为数量值.
    关于分页：如果DB中的数量大于N，返回json会携带一个字段“cursor”,我们把它叫做”游标”，
    该游标可理解为结果集的指针，值是变化的。往下取数据的时候带着游标，就可以获取到下一页的值。
    如果还有下一页，返回值里依然还有这个字段，直到没有这个字段，说明已经到最后一页。
    cursor的意义在于数据(真)分页。

    未分页：
    Path : /{org_name}/{app_name}/users
    HTTP Method : GET
    URL Params ： limit=20
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ： 无
    Response Body

    分页：
    Path : /{org_name}/{app_name}/users
    HTTP Method : GET
    URL Params ： limit=20&cursor=LTU2ODc0MzQzOnNmdTlxdF9LRWVPaVFvMWlBZmc4S3c
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ： 无
    """
    def get_users(self, limit,cursor=None):
        pass


    """
    Path : /{org_name}/{app_name}/users/{username}
    HTTP Method : DELETE
    URL 参数 : 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ： 无
    """
    def del_user(self, username):
        token = self.easemob_get_token()
        url = endpoint + appurl + "/users/" + username
        payload = {'username': username}

        success, result = self.easemob_request(url, "DELETE", payload, auth=token)
        self.logger.info("del_user reulst is %s " % result)

        return result


    """
    Path : /{org_name}/{app_name}/users/{username}/password
    HTTP Method : PUT
    URL Params : 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ： {“newpassword” : “${新密码指定的字符串}”}
    """
    def reset_passwd(self, username, passwd):
        pass


    """
    Path : /{org_name}/{app_name}/users/{username}
    HTTP Method : PUT
    URL Params : 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ： {“nickname” : “${昵称值}”}
    """
    def change_nickname(self, username, nickname):
        pass


    """
    Path : /{org_name}/{app_name}/users/{owner_username}/contacts/users/{friend_username}
    HTTP Method : POST
    URL Params : 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ： 无
    """
    def add_friend(self, username, friend_username):
        pass


    """
    Path : /{org_name}/{app_name}/users/{owner_username}/contacts/users/{friend_username}
    HTTP Method : DELETE
    URL Params : 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ： 无
    """
    def del_friend(self, username, friend_username):
        pass


    """
    Path : /{org_name}/{app_name}/users/{owner_username}/contacts/users
    HTTP Method : GET
    URL Params : 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ： 无
    """
    def get_friends(self, username):
        pass


    """
    Path : /{org_name}/{app_name}/users/{owner_username}/blocks/users
    HTTP Method : GET
    URL Params : 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ： 无
    """
    def get_blacklists(self, username):
        pass


    """
    Path : /{org_name}/{app_name}/users/{owner_username}/blocks/users
    HTTP Method : POST
    URL Params : 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ： {“usernames”:[“5cxhactgdj”, “mh2kbjyop1”]} —- 需要加入到黑名单中的用户名以数组方式提交，usernames为关键字不变，
    Response Body ： “data” : [ “5cxhactgdj”, “mh2kbjyop1” ] — 已经加到黑名单中的用户名：5cxhactgdj, mh2kbjyop1
    """
    def blacklist_one(self, username, blacklist_users):
        pass

    """
    Path : /{org_name}/{app_name}/users/{owner_username}/blocks/users/{blocked_username}
    HTTP Method : DELETE
    URL Params : 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ：无
    Response Body ： entities 中包含了刚刚从黑名单中移除的IM用户的详细信息
    """
    def unblacklist_one(self, username, blacklist_user):
        pass


    """
    Path : /{org_name}/{app_name}/users/{username}/status
    HTTP Method : GET
    URL Params ： 无
    Request Headers : {“Content-Type”:”application/json”,”Authorization”:”Bearer ${token}”}
    Request Body ：
    "data": {
            "stliu": "online"  //注意, 这里返回的是用户名和在线状态的键值对, 值为 online 或者 offline
        }
    """
    def check_online(self, username):
        pass


    """
    Path : /{org_name}/{app_name}/users/{owner_username}/offline_msg_count
    HTTP Method : GET
    URL Params : 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ： 无
    Response Body ： “data” : {“v3y0kf9arx” : 0 } —- 用户名：v3y0kf9arx ，离线消息数：0条
    """
    def offline_msg_count(self, username):
        pass

    """
    Path : /{org_name}/{app_name}/users/{username}/offline_msg_status/{msg_id}
    HTTP Method : GET
    URL Params ： 无
    Request Headers : {“Content-Type”:”application/json”,”Authorization”:”Bearer ${token}”}
    Request Body ： 无
    Response Body ： 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略。
    """
    def offline_msg_status(self, username, msg_id):
        pass

    """
    Path : /{org_name}/{app_name}/users/{username}/deactivate
    HTTP Method : POST
    URL Params ： 无
    Request Headers : {“Content-Type”:”application/json”,”Authorization”:”Bearer ${token}”}
    Request Body ： 无
    Response Body ： 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略
    """
    def deactivate_user(self, username):
        pass

    """
    Path : /{org_name}/{app_name}/users/{username}/activate
    HTTP Method : POST
    URL Params ： 无
    Request Headers : {“Content-Type”:”application/json”,”Authorization”:”Bearer ${token}”}
    Request Body ： 无
    Response Body ： 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略。
    """
    def activate_user(self, username):
        pass

    """
    Path : /{org_name}/{app_name}/users/{username}/disconnect
    HTTP Method : GET
    URL Params ： 无
    Request Headers : {“Content-Type”:”application/json”,”Authorization”:”Bearer ${token}”}
    Request Body ： 无
    """
    def disconnect_user(self, username):
        pass


    ##################################################################################
    #######################File upload/download#######################################
    ##################################################################################
    """
    注意，上传文件大小不能超过10M,超过会上传失败
    Path : /{org_name}/{app_name}/chatfiles
    HTTP Method : POST
    Request Headers : {“restrict-access”:true,”Authorization”:”Bearer ${token}”}
    URL Params ： 无
    Request Body ：文件表单项 参考
    需要使用http multipart/form-data 形式
    curl --verbose --header "Authorization: Bearer YWMtz1hFWOZpEeOPpcmw1FB0RwAAAUZnAv0D7y9-i4c9_c4rcx1qJDduwylRe7Y"
    --header "restrict-access:true" --form file=@/Users/stliu/a.jpg https://a1.easemob.com/easemob-demo/chatdemoui/chatfiles
    """
    def upload_file(self, username, file):
        pass

    """
    下载图片语音文件
    curl -O -H "share-secret: DRGM8OZrEeO1vafuJSo2IjHBeKlIhDp0GCnFu54xOF3M6KLr"
    --header "Authorization: Bearer YWMtz1hFWOZpEeOPpcmw1FB0RwAAAUZnAv0D7y9-i4c9_c4rcx1qJDduwylRe7Y"
    -H "Accept: application/octet-stream"
    https://a1.easemob.com/easemob-demo/chatdemoui/chatfiles/0c0f5f3a-e66b-11e3-8863-f1c202c2b3ae

    下载缩略图
    curl -O -H "thumbnail: true" -H "share-secret: DRGM8OZrEeO1vafuJSo2IjHBeKlIhDp0GCnFu54xOF3M6KLr"
    -H "Authorization: Bearer YWMtz1hFWOZpEeOPpcmw1FB0RwAAAUZnAv0D7y9-i4c9_c4rcx1qJDduwylRe7Y"
    -H "Accept: application/octet-stream"
    https://a1.easemob.com/easemob-demo/chatdemoui/chatfiles/0c0f5f3a-e66b-11e3-8863-f1c202c2b3ae
    """
    def download_file(self, username, file_uuid):
        pass

    ##################################################################################
    #######################Message####################################################
    ##################################################################################
    """
    发送文本消息
    给一个或者多个用户, 或者一个或者多个群组发送消息, 并且通过可选的 from 字段让接收方看到发送方
    是不同的人,同时, 支持扩展字段, 通过 ext 属性, app可以发送自己专属的消息结构.
    Path : /{org_name}/{app_name}/messages
    Request Method : POST
    URL Params ： 无
    Request Headers : {“Content-Type”:”application/json”,”Authorization”:”Bearer ${token}”}
    {
        "target_type" : "users", // users 给用户发消息, chatgroups 给群发消息
        "target" : ["u1", "u2", "u3"], // 注意这里需要用数组,数组长度建议不大于20, 即使只有一个用户,
                                       // 也要用数组 ['u1'], 给用户发送时数组元素是用户名,给群组发送时
                                       // 数组元素是groupid
        "msg" : {
            "type" : "txt",
            "msg" : "hello from rest" //消息内容，参考[[start:100serverintegration:30chatlog|聊天记录]]里的bodies内容
            },
        "from" : "jma2", //表示这个消息是谁发出来的, 可以没有这个属性, 那么就会显示是admin, 如果有的话, 则会显示是这个用户发出的
        "ext" : { //扩展属性, 由app自己定义.可以没有这个字段，但是如果有，值不能是“ext:null“这种形式，否则出错
            "attr1" : "v1",
            "attr2" : "v2"
        }
    }
    """
    def send_txt_msg(self, user_name, msg_body):
        pass

    """
    发送图片消息
    给一个或者多个用户, 或者一个或者多个群组发送消息, 并且通过可选的 from 字段让接收方看到发送方
    是不同的人,同时, 支持扩展字段, 通过 ext 属性, app可以发送自己专属的消息结构.
    Path : /{org_name}/{app_name}/messages
    Request Method : POST
    URL Params ： 无
    Request Headers : {“Content-Type”:”application/json”,”Authorization”:”Bearer ${token}”}
    Response Body ： 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略。
    Request Body ：
    {
        "target_type" : "users",   //users 给用户发消息, chatgroups 给群发消息
        "target" : ["u1", "u2", "u3"],// 注意这里需要用数组,数组长度建议不大于20, 即使只有一个用户,
                                      // 也要用数组 ['u1'], 给用户发送时数组元素是用户名,给群组发送时
                                      // 数组元素是groupid
        "msg" : {  //消息内容
            "type" : "img",   // 消息类型
            "url": "https://a1.easemob.com/easemob-demo/chatdemoui/chatfiles/55f12940-64af-11e4-8a5b-ff2336f03252",  //成功上传文件返回的uuid
            "filename": "24849.jpg", // 指定一个文件名
            "secret": "VfEpSmSvEeS7yU8dwa9rAQc-DIL2HhmpujTNfSTsrDt6eNb_", // 成功上传文件后返回的secret
            "size" : {
              "width" : 480,
              "height" : 720
          }
         },
        "from" : "jma2", //表示这个消息是谁发出来的, 可以没有这个属性, 那么就会显示是admin, 如果有的话, 则会显示是这个用户发出的
        "ext" : { //扩展属性, 由app自己定义.可以没有这个字段，但是如果有，值不能是“ext:null“这种形式，否则出错
            "attr1" : "v1",
            "attr2" : "v2"
        }
    }

    """
    def send_img_msg(self, username, msg_body):
        pass

    """
    发送语音消息
    发送语音文件，需要先上传语音文件，然后再发送此消息。（url中的uuid和secret可以从上传后的response获取
    Path : /{org_name}/{app_name}/messages
    Request Method : POST
    URL Params ： 无
    Request Headers : {“Content-Type”:”application/json”,”Authorization”:”Bearer ${token}”}
    Request Body ：

    {
        "target_type" : "users",  //users 给用户发消息, chatgroups 给群发消息
        "target" : ["testd", "testb", "testc"],// 注意这里需要用数组,数组长度建议不大于20, 即使只有一个
                                               // 用户或者群组, 也要用数组形式 ['u1'], 给用户发送
                                               // 此数组元素是用户名,给群组发送时数组元素是groupid
        "msg" : {   //消息内容
            "type": "audio",  // 消息类型
            "url": "https://a1.easemob.com/easemob-demo/chatdemoui/chatfiles/1dfc7f50-55c6-11e4-8a07-7d75b8fb3d42",  //成功上传文件返回的uuid
            "filename": "messages.amr", // 指定一个文件名
            "length": 10,
            "secret": "Hfx_WlXGEeSdDW-SuX2EaZcXDC7ZEig3OgKZye9IzKOwoCjM" // 成功上传文件后返回的secret
        },
        "from" : "testa" ,  //表示这个消息是谁发出来的, 可以没有这个属性, 那么就会显示是admin, 如果有的话, 则会显示是这个用户发出的
        "ext" : { //扩展属性, 由app自己定义.可以没有这个字段，但是如果有，值不能是“ext:null“这种形式，否则出错
                "attr1" : "v1",
                "attr2" : "v2"
        }
    }
    """
    def send_audio_msg(self, username, msg_body):
        pass

    """
    发送视频消息
    发送视频消息，需要先上传视频文件和视频缩略图文件，然后再发送此消息。（url中的uuid和secret可以从上传后的response获取）
    Path : /{org_name}/{app_name}/messages
    Request Method : POST
    URL Params ： 无
    Request Headers : {“Content-Type”:”application/json”,”Authorization”:”Bearer ${token}”}
    Request Body ：

    {
        "target_type": "users", //users 给用户发消息, chatgroups 给群发消息
        "target": [
            "ceshib"// 注意这里需要用数组,数组长度建议不大于20, 即使只有一个，// 用户或者群组, 也要用数组形式 ['u1'], 给用户发送
        ], // 此数组元素是用户名,给群组发送时数组元素是groupid
        "from": "ceshia",
        "msg": { //消息内容
            "type": "video",// 消息类型
            "filename": "1418105136313.mp4",// 视频文件名称
            "thumb": "https://a1.easemob.com/easemob-demo/chatdemoui/chatfiles/67279b20-7f69-11e4-8eee-21d3334b3a97",//成功上传视频缩略图返回的uuid
            "length": 10,//视频播放长度
            "secret": "VfEpSmSvEeS7yU8dwa9rAQc-DIL2HhmpujTNfSTsrDt6eNb_",// 成功上传视频文件后返回的secret
            "file_length": 58103,//视频文件大小
            "thumb_secret": "ZyebKn9pEeSSfY03ROk7ND24zUf74s7HpPN1oMV-1JxN2O2I",// 成功上传视频缩略图后返回的secret
            "url": "https://a1.easemob.com/easemob-demo/chatdemoui/chatfiles/671dfe30-7f69-11e4-ba67-8fef0d502f46"//成功上传视频文件返回的uuid
        }
    }
    """
    def send_video_msg(self, username, msg_body):
        pass

    """
    发送透传消息
    透传消息：不会在客户端提示（铃声，震动，通知栏等），但可以在客户端监听到的消息推送，具体功能可以根据自身自定义
    Path : /{org_name}/{app_name}/messages
    Request Method : POST
    URL Params ： 无
    Request Headers : {“Content-Type”:”application/json”,”Authorization”:”Bearer ${token}”}
    Request Body ：

    {
        "target_type":"users",     // users 给用户发消息,  chatgroups 给群发消息
        "target":["testb","testc"], // 注意这里需要用数组,数组长度建议不大于20, 即使只有
                                    // 一个用户u1或者群组, 也要用数组形式 ['u1'], 给用户发
                                    // 送时数组元素是用户名,给群组发送时数组元素是groupid
        "msg":{  //消息内容
            "type":"cmd",  // 消息类型
            "action":"action1"
        },
        "from":"testa",  //表示这个消息是谁发出来的, 可以没有这个属性, 那么就会显示是admin, 如果有的话, 则会显示是这个用户发出的
        "ext":{   //扩展属性, 由app自己定义.可以没有这个字段，但是如果有，值不能是“ext:null“这种形式，否则出错
            "attr1":"v1",
            "attr2":"v2"
        }
    }
    """
    def send_cmd_msg(self, username, msg_body):
        pass



    ##################################################################################
    #######################Group######################################################
    ##################################################################################
    """
    Path : /{org_name}/{app_name}/chatgroups
    HTTP Method : GET
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ：
    Response Body ： 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略。
    """
    def get_chatgroups(self, username):
        pass

    """
    分页获取app下的群组
    Path : /{org_name}/{app_name}/chatgroups
    HTTP Method : GET
    URL Params ： limit 预期获取的记录数，数字类型; cursor　游标，如果数据还有下一页，api返回值会包含此字段, 字符类型．
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ：
    """
    def get_chatgroups_bypages(self, username):
        pass

    """
    Path : /{org_name}/{app_name}/chatgroups/{group_id1},{group_id2}
    HTTP Method : GET
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    """
    def get_group_detail(self, username, group_ids):
        pass

    """
    Path : /{org_name}/{app_name}/chatgroups
    HTTP Method : POST
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ：
    {
        "groupname":"testrestgrp12", //群组名称, 此属性为必须的
        "desc":"server create group", //群组描述, 此属性为必须的
        "public":true, //是否是公开群, 此属性为必须的
        "maxusers":300, //群组成员最大数(包括群主), 值为数值类型,默认值200,此属性为可选的
        "approval":true, //加入公开群是否需要批准, 默认值是true（加群需要群主批准）, 此属性为可选的
        "owner":"jma1", //群组的管理员, 此属性为必须的
        "members":["jma2","jma3"] //群组成员,此属性为可选的,但是如果加了此项,数组元素至少一个（注：群主jma1不需要写入到members里面）
    }
    """
    def create_chatgroup(self, username, group_body=None):
        token = self.easemob_get_token()
        url = endpoint + appurl + "/chatgroups"
        payload = group_body

        success, result = self.easemob_request(url, "POST", payload, auth=token)
        self.logger.info("del_user reulst is %s " % result)

        return result

    """
    Path : /{org_name}/{app_name}/chatgroups/{group_id}
    HTTP Method : PUT
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ：
    {
        "groupname":"testrestgrp12", //群组名称，修改时值不能包含斜杠( "/")
        "description":"update groupinfo", //群组描述，修改时值不能包含斜杠( "/")
        "maxusers":300, //群组成员最大数(包括群主), 值为数值类型
    }
    """
    def change_chatgroup(self, username, group_body):
        pass

    """
    Path : /{org_name}/{app_name}/chatgroups/{group_id}
    HTTP Method : DELETE
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    """
    def del_chatgroup(self, group_id):
        pass

    """
    Path : /{org_name}/{app_name}/chatgroups/{group_id}/users
    HTTP Method : GET
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    """
    def getusers_in_chatgroup(self, group_id):
        pass

    """
    Path : /{org_name}/{app_name}/chatgroups/{group_id}/users/{username}
    HTTP Method : POST
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    """
    def add_member_to_chatgroup(self, username, group_id, new_user):
        pass

    """
    Path : /{org_name}/{app_name}/chatgroups/{chatgroupid}/users
    HTTP Method : POST
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ：{“usernames”:[“username1”,”username2”]}’
    — usernames固定属性，作为json的KEY；username1/username2 要添加到群中的成员用户名，可变
    """
    def add_members_to_chatgroup(self, username, group_id, new_users):
        pass

    """
    Path : /{org_name}/{app_name}/chatgroups/{group_id}/users/{username}
    HTTP Method : DELETE
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    """
    def del_member_from_chatgroup(self, username, group_id, del_user):
        pass

    """
    Path : /{org_name}/{app_name}/chatgroups/{group_id}/users/memeber1,member2,member3
    HTTP Method : DELETE
    URL Params ： 无
    Request Headers : {“Content-Type”:“application/json”,“Authorization”:“Bearer ${token}”}
    Request Body ： 无
    Response Body ： result为true表示移除成功;result为false表示移除失败，此时reason字段注明失败原因．
    """
    def del_members_from_chatgroup(self, username, group_id, del_users):
        pass

    """
    Path : /{org_name}/{app_name}/users/{username}/joined_chatgroups
    HTTP Method : GET
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    """
    def get_userjoined_chatgroups(self, username):
        pass

    """
    修改群组Owner为同一App下的存在用户
    Path : /{org_name}/{app_name}/chatgroups/{groupid}
    HTTP Method : PUT
    URL Params ： 无
    Request Headers : {“Content-Type”:“application/json”,“Authorization”:“Bearer ${token}”}
    Request Body ： {“newowner”:“${new_owner_user}”}
    """
    def change_chatgroup_owner(self, username, newowner):
        pass

    """
    查询一个群组黑名单用户名列表
    Path : /{org_name}/{app_name}/chatgroups/{group_id}/blocks/users
    HTTP Method : GET
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    """
    def getblacklist_of_chatgroup(self, group_id):
        pass

    """
    添加一个用户进入一个群组的黑名单
    Path : /{org_name}/{app_name}/chatgroups/{group_id}/blocks/users/{username}
    HTTP Method : POST
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    """
    def addblacklist_to_chatgroup(self, username, group_id, black_user):
        pass

    """
    添加多个用户进入一个群组的黑名单
    Path : /{org_name}/{app_name}/chatgroups/{group_id}/blocks/users
    HTTP Method : POST
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ： {“usernames”:[“username1”,“username2”,“username3”]}
    Response Body ： result表示添加结果: true 成功, false 失败, 失败时会标明原因
    """
    def addblacklists_to_chatgroup(self, username, group_id, black_users):
        pass

    """
    从群组黑名单中删除一个用户
    Path : /{org_name}/{app_name}/chatgroups/{group_id}/blocks/users/{username}
    HTTP Method : DELETE
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ： 无
    Response Body ： result表示添加结果: true 成功, false 失败, 失败时会标明原因
    """
    def delblacklist_from_chatgroup(self, username, group_id, black_user):
        pass

    """
    从群组黑名单中删除多个用户
    Path : /{org_name}/{app_name}/chatgroups/{group_id}/blocks/users/{username1},{username2}
    HTTP Method : DELETE
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ： 无
    Response Body ： result表示添加结果: true 成功, false 失败, 失败时会标明原因
    """
    def delblacklists_from_chatgroup(self, username, group_id, black_users):
        pass

    ##################################################################################
    #######################Chat room##################################################
    ##################################################################################
    """
    创建聊天室
    Path : /{org_name}/{app_name}/chatrooms
    HTTP Method : POST
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ：
     {
        "name":"testchatroom", //聊天室名称, 此属性为必须的
        "description":"server create chatroom", //聊天室描述, 此属性为必须的
        "maxusers":300, //聊天室成员最大数(包括群主), 值为数值类型,默认值200,此属性为可选的
        "owner":"jma1", //聊天室的管理员, 此属性为必须的
        "members":["jma2","jma3"] //聊天室成员,此属性为可选的,但是如果加了此项,数组元素至少一个（注：群主jma1不需要写入到members里面）
    }
    """
    def create_chatroom(self, username, chatroom_body):
        pass

    """
    修改聊天室信息
    Path : /{org_name}/{app_name}/chatrooms/{chatroom_id}
    HTTP Method : PUT
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ：
       {
        "name":"test chatroom", //聊天室名称
        "description":"update chatroominfo", //聊天室描述
        "maxusers":200, //聊天室成员最大数(包括群主), 值为数值类型
       }
    """
    def change_chatroom(self, username, chatroom_id, chatroom_body):
        pass

    """
    删除聊天室
    Path : /{org_name}/{app_name}/chatrooms/{chatroom_id}
    HTTP Method : DELETE
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ：无
    Response Body ： 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略。
    """
    def del_chatroom(self, username, chatroom_id):
        pass

    """
    获取app中所有的聊天室
    Path :/{org_name}/{app_name}/chatrooms
    HTTP Method : GET
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    """
    def get_all_chatrooms(self, ):
        pass

    """
    获取一个聊天室详情
    Path : /{org_name}/{app_name}/chatrooms/{chatroom_id}
    HTTP Method : GET
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    """
    def get_one_chatroom(self, chatroom_id):
        pass

    """
    获取用户加入的聊天室
    Path : /{org_name}/{app_name}/users/{username}/joined_chatrooms
    HTTP Method : GET
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    """
    def get_userjoined_chatrooms(self, username):
        pass

    """
    聊天室成员添加[单个]
    Path : /{org_name}/{app_name}/chatrooms/{chatroomid}/users/{username}
    HTTP Method : POST
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ： 无
    Response Body ： result 表示添加结果：true 添加成功，false　添加失败
    可能的错误码： 404 （此群组id不存在） 401（未授权[无token,token错误,token过期]） 5xx 详见：服务器端REST API常见错误码
    """
    def adduser_to_chatroom(self, username, chatroomid):
        pass

    """
    聊天室成员添加[批量]
    Path : /{org_name}/{app_name}/chatrooms/{chatroomid}/users
    HTTP Method : POST
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ： {“usernames”:[“username1”, “username2”]}
    Response Body ： 请求成功会返回被加入聊天室中的新成员username
    """
    def addusers_to_chatroom(self, userslist, chatroomid):
        pass

    """
    聊天室成员删除[单个]
    Path : /{org_name}/{app_name}/chatrooms/{chatroomid}/users/{username}
    HTTP Method : DELETE
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ： 无
    Response Body ： result 表示添加结果：true 添加成功，false　添加失败
    """
    def deluser_from_chatroom(self, username, chatroomid):
        pass

    """
    聊天室成员删除[批量]
    Path : /{org_name}/{app_name}/chatrooms/{chatroomid}/users/{username1},{username2}
    HTTP Method : DELETE
    URL Params ： 无
    Request Headers : {“Authorization”:”Bearer ${token}”}
    Request Body ： 无
    Response Body ： result 表示添加结果：true 添加成功，false　添加失败，添加失败的原因会描述在reason字段中．
    """
    def deluser_from_chatroom(self, userslist, chatroomid):
        pass

##################################################################################
#######################Chat record################################################
##################################################################################




##################################################################################
#######################Test#######################################################
##################################################################################
if __name__ == '__main__':
    #when test,you must cd /home/jincm/zuohaoshi/server first,also is myapp's parent dir
    #and then "sudo python myapp/ext/easemob.py"
    import logging
    import random

    logger = logging.getLogger()
    fh = logging.FileHandler('/tmp/easemob.log', 'a+')
    logger.addHandler(fh)
    logger.setLevel(logging.DEBUG)

    im_obj = EasemobIM(logger)
    token = im_obj.easemob_get_token()

    for i in xrange(1, 10):
        username = str(random.randint(11111,99999))
        im_obj.register_user(username, '123456', nickname=username)

        im_obj.del_user(username)

    #im_obj.register_users(userslist)
    #im_obj.get_user(username)
    #im_obj.get_users(limit,cursor=None)


    #im_obj.send_txt_msg(username, msg_body)

    group_body = {}
    group_body['groupname'] = 'testgroup'
    group_body['desc'] = 'server'
    group_body['public'] = True
    group_body['owner'] = '76439'
    im_obj.create_chatgroup(username, group_body)

    #im_obj.create_chatroom(username, chatroom_body)

    """

    #
    im_obj.reset_passwd(username, passwd)
    im_obj.change_nickname(username, nickname)
    im_obj.add_friend(username, friend_username)
    im_obj.del_friend(username, friend_username)
    im_obj.get_friends(username)
    """

    """
    im_obj.get_blacklists(username)
    im_obj.blacklist_one(username, blacklist_users)
    im_obj.unblacklist_one(username, blacklist_user)
    im_obj.check_online(username)
    im_obj.offline_msg_count(username)
    im_obj.offline_msg_status(username, msg_id)
    im_obj.deactivate_user(username)
    im_obj.activate_user(username)
    im_obj.disconnect_user(username)

    im_obj.upload_file(username, file)
    im_obj.download_file(username, file_uuid)


    im_obj.send_img_msg(username, msg_body)
    im_obj.send_audio_msg(username, msg_body)
    im_obj.send_video_msg(username, msg_body)
    im_obj.send_cmd_msg(username, msg_body)

    im_obj.get_chatgroups(username)
    im_obj.get_chatgroups_bypages(username)
    im_obj.get_group_detail(username, group_ids)

    im_obj.change_chatgroup(username, group_body)
    im_obj.del_chatgroup(group_id)
    im_obj.getusers_in_chatgroup(group_id)
    im_obj.add_member_to_chatgroup(username, group_id, new_user)
    im_obj.add_members_to_chatgroup(username, group_id, new_users)
    im_obj.del_member_from_chatgroup(username, group_id, del_user)
    im_obj.del_members_from_chatgroup(username, group_id, del_users)
    im_obj.get_userjoined_chatgroups(username)
    im_obj.change_chatgroup_owner(username, newowner)
    im_obj.getblacklist_of_chatgroup(group_id)
    im_obj.addblacklist_to_chatgroup(username, group_id, black_user)
    im_obj.addblacklists_to_chatgroup(username, group_id, black_users)
    im_obj.delblacklist_from_chatgroup(username, group_id, black_user)
    im_obj.delblacklists_from_chatgroup(username, group_id, black_users)

    im_obj.create_chatroom(username, chatroom_body)
    im_obj.change_chatroom(username, chatroom_id, chatroom_body)
    im_obj.del_chatroom(username, chatroom_id)
    im_obj.get_all_chatrooms()
    im_obj.get_one_chatroom(chatroom_id)
    im_obj.get_userjoined_chatrooms(username)
    im_obj.adduser_to_chatroom(username, chatroomid)
    im_obj.addusers_to_chatroom(userslist, chatroomid)
    im_obj.deluser_from_chatroom(username, chatroomid)
    im_obj.deluser_from_chatroom(userslist, chatroomid)
    """


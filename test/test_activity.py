#!/usr/bin/env python

# coding = "utf-8"

"""
    zuohaoshi test module
    Good man is well
"""
import os
import sys
import time
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
import random
import json

import requests

from test_user import myrequest

##################################################################################
#######################Test#######################################################
##################################################################################
# kill -9 `pidof uwsgi` && sleep 2 && /usr/local/bin/uwsgi /home/jincm/zuohaoshi/server/uwsgi_config.ini
# python zuohaoshi/server/test/test_activity.py 192.168.3.12 80
if __name__ == '__main__':
    logger = logging.getLogger()
    logfile = '/tmp/test.log'
    file_handler = RotatingFileHandler(logfile, 'a', 100*1024*1024, 10)
    file_handler.setFormatter(Formatter('[%(process)d %(filename)s:%(lineno)d]%(asctime)s:\n %(message)s'))
    logger.addHandler(file_handler)
    # fh = logging.FileHandler(logfile, 'a+')
    # logger.addHandler(fh)
    logger.setLevel(logging.INFO)

    HOST = '127.0.0.1'
    PORT = '8000'
    VER = '/v1'

    ADMIN = '/admin'
    USERS = '/u'
    ACTIVITY = '/ay'
    GROUP = '/g'
    TEST_COUNT = 1

    if len(sys.argv) > 1:
        HOST = sys.argv[1]
    if len(sys.argv) > 2:
        PORT = sys.argv[2]
    if len(sys.argv) > 3:
        TEST_COUNT = int(sys.argv[3])

    URL = 'http://' + HOST + ':' + PORT + VER
    logger.info(URL)

    # user
    print "###############################################"
    print "#######User test begin#############"
    print "###############################################"
    # #####user login#########
    my_url = URL + USERS + "/login"
    my_headers = {'content-type': 'application/json'}
    payload = dict()
    payload['account'] = '123456789'
    payload['passwd'] = '123456'

    ret = myrequest(my_url, "POST", headers=my_headers, payload=payload)
    if ret:
        user_id = ret.get('user_id')
        token = ret.get('token')
        if user_id is None or token is None:
            print "POST ERROR:resp error:%s\n" % ret
            exit(1)
    else:
        exit(1)

    # activity
    print "###############################################"
    print "#######activity test begin#############"
    print "###############################################"
    """
    # post add
    my_url = URL + ACTIVITY + "/lost/" + "post"
    my_headers = dict()
    my_headers['content-type'] = 'application/json'
    my_headers['token'] = token
    payload = dict()
    payload['content'] = 'test for post lost type'
    payload['loc'] = [1.1, 2.2]

    ret = myrequest(my_url, "POST", headers=my_headers, payload=payload)
    if ret:
        post_id = ret.get('post_id')
        if post_id is None:
            print "POST ERROR:resp error:%s\n" % ret
            exit(1)
    else:
        exit(1)

    # post add pictures
    my_url = URL + ACTIVITY + "/lost/" + post_id + "/upload_imgs"
    params = dict()
    params['token'] = token
    # upload file
    file1 = '/home/jincm/zuohaoshi/server/test/1.png'
    file2 = '/home/jincm/zuohaoshi/server/test/2.jpg'
    myfiles = {'file1': open(file1, 'rb'), 'file2': open(file2, 'rb')}
    print "POST:%s?files:%s" % (my_url, myfiles)

    ret = myrequest(my_url, "POST", params=params, files=myfiles)
    if ret:
        check_key = ret.get('post_id')
        if check_key is None:
            print "POST ERROR:%s?head:%s,resp:%s\n" % (my_url, params, ret)
            exit(1)
    else:
        exit(1)

    # post_id = "563ed050ce6a3d1f234f3eba"
    # token = "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0Njk2MzEzNiwiaWF0IjoxNDQ2OTU3MTM2fQ.eyJwYXNzd2QiOiIxMjM0NTYiLCJ1c2VyX2lkIjoiMTAwMDIifQ.HyJlPUW6ERDBCoEBB4M3b2fjbEzyXN2JL84DXMS0ePg"

    # get post by id
    my_url = URL + ACTIVITY + "/lost/" + post_id
    params = dict()
    params['token'] = token
    ret = myrequest(my_url, "GET", params=params)
    if ret:
        check_key = ret.get('_id')
        if check_key is None:
            print "GET ERROR:%s?head:%s,resp:%s\n" % (my_url, my_headers, ret)
            exit(1)
    else:
        exit(1)

    # comment for post
    my_url = URL + ACTIVITY + "/lost/" + post_id + "/comment"
    my_headers = dict()
    my_headers['content-type'] = 'application/json'
    my_headers['token'] = token
    payload = dict()
    payload['praise'] = 1
    payload['comment'] = 'test for post comment 2222222'

    ret = myrequest(my_url, "POST", headers=my_headers, payload=payload)
    if ret:
        comment_id = ret.get('comment_id')
        if comment_id is None:
            print "POST ERROR:%s?head:%s,resp:%s\n" % (my_url, my_headers, ret)
            exit(1)
    else:
        exit(1)

    # delete comment for post by comment_id
    my_url = URL + ACTIVITY + "/lost/" + post_id + "/" + comment_id
    params = dict()
    params['token'] = token

    ret = myrequest(my_url, "DELETE", params=params)
    if ret:
        check_key = ret.get('post_id')
        if check_key is None:
            print "DELETE ERROR:%s?head:%s,resp:%s\n" % (my_url, my_headers, ret)
            exit(1)
    else:
        exit(1)

    # delete post by id
    my_url = URL + ACTIVITY + "/lost/" + post_id
    params = dict()
    params['token'] = token

    ret = myrequest(my_url, "DELETE", params=params)
    if ret:
        check_key = ret.get('post_id')
        if check_key is None:
            print "DELETE ERROR:%s?head:%s,resp:%s\n" % (my_url, my_headers, ret)
            exit(1)
    else:
        exit(1)
    """

    # get user's posts
    # post add
    for loop in xrange(1, 4):
        time.sleep(1)
        my_url = URL + ACTIVITY + "/lost/" + "post"
        my_headers = dict()
        my_headers['content-type'] = 'application/json'
        my_headers['token'] = token
        payload = dict()
        payload['content'] = 'test for post lost type' + '%s' % loop
        payload['loc'] = [1.1, 2.2]

        ret = myrequest(my_url, "POST", headers=my_headers, payload=payload)
        if ret:
            post_id = ret.get('post_id')
            if post_id is None:
                print "POST ERROR:resp error:%s\n" % ret
                exit(1)
        else:
            exit(1)

    # get one user's posts
    uid = '10002'
    my_url = URL + ACTIVITY + "/" + uid + "/lost/posts"
    params = dict()
    params['token'] = token
    params['offset'] = 2
    params['limit'] = 11
    ret = myrequest(my_url, "GET", params=params)
    if ret:
        check_key = ret.get('posts')
        if check_key is None:
            print "GET ERROR:%s?params:%s,resp:%s\n" % (my_url, params, ret)
            exit(1)
    else:
        exit(1)

    # search posts by conditions: loc=x,y&age=19&sex=man&fields=age,name,head_img&offset=10&limit=5
    post_type = "update"
    my_url = URL + ACTIVITY + "/search/" + post_type
    my_headers = dict()
    my_headers['content-type'] = 'application/json'
    my_headers['token'] = token

    payload = dict()
    # payload['token'] = token
    payload['loc'] = "11,22"
    # payload['age'] = 18
    payload['sex'] = "man"
    payload['fields'] = "age,name,head_img"
    payload['offset'] = 2
    payload['limit'] = 8

    ret = myrequest(my_url, "POST", headers=my_headers, payload=payload)
    if ret:
        check_key = ret.get('posts')
        if check_key is None:
            print "GET ERROR:%s?params:%s,resp:%s\n" % (my_url, payload, ret)
            exit(1)
    else:
        exit(1)

    # lost

    print "###############################################"
    print "#######exit OK#############"
    print "###############################################"





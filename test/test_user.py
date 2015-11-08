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


def myrequest(url, method, headers=None, params=None, payload=None, files=None):
    try:
        if method == 'GET':
            print "%s:%s?header:%s?params:%s" % (method, url, headers, params)
            resp = requests.get(url, params=params, headers=headers)

            if resp.status_code == 200:
                print "%s OK:%s?header:%s?%s\nresp:[%s]\n" % (method, url, headers, params,resp.json())
                return resp.json()
            else:
                print "%s ERROR:%s?header:%s?%s;resp:%s\n" % (method, url, headers, params, resp.text)
                return None
        elif method == 'POST':
            if files is None:
                print "%s:%s?header:%s?%s" % (method, url, headers, payload)
                resp = requests.post(url, data=json.dumps(payload), headers=headers)

                if resp.status_code == 200:
                    print "%s OK:%s?header:%s?%s\nresp:[%s]\n" % (method, url, headers, payload, resp.json())
                    return resp.json()
                else:
                    print "%s ERROR:%s?header:%s?%s;resp:%s\n" % (method, url, headers, payload, resp.text)
                    return None
            else:  # post files
                print "%s:%s?%s,files:%s" % (method, url, params, files)
                resp = requests.post(url, params=params, files=files)

                if resp.status_code == 200:
                    print "%s OK:%s?files:%s?%s\nresp:[%s]\n" % (method, url, files, params, resp.json())
                    return resp.json()
                else:
                    print "%s ERROR:%s?files:%s?%s;resp:%s\n" % (method, url, files, params, resp.text)
                    return None
        elif method == 'DELETE':
            print "%s:%s?header:%s?%s" % (method, url, headers, params)
            resp = requests.delete(url, params=params)

            if resp.status_code == 200:
                print "%s OK:%s?header:%s?%s\nresp:[%s]\n" % (method, url, headers, params, resp.json())
                return resp.json()
            else:
                print "%s ERROR:%s?header:%s?%s;resp:%s\n" % (method, url, headers, params, resp.text)
                return None
        else:
            logger.info("request no method\n")
            return None
    except Exception, e:
        print "%s ERROR except:%s?header:%s?%s,%s" % (method, url, headers, params, payload)
        return None

# sudo kill -9 `pidof uwsgi`
# sudo /usr/local/bin/uwsgi /home/jincm/zuohaoshi/server/uwsgi_config.ini
##################################################################################
#######################Test#######################################################
##################################################################################
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
    VER = '/1'

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

    for loop in xrange(1, TEST_COUNT):
        # ######get identify code#
        try:
            my_url = URL + USERS + "/register"
            rand_num = str(random.randint(1111, 9999))
            payload = dict()
            payload['account'] = '1234567' + rand_num
            print "GET:%s?%s" % (my_url, payload)

            resp = requests.get(my_url, params=payload)
            logger.info("GET:%s?%s,response:%s\n", my_url, payload, resp.json())
        except Exception, e:
            logger.error("GET ERROR:%s?%s,error:%s\n", my_url, payload, e)
            exit(1)
        else:
            print 'resp:%s\n' % resp.text
            if resp.status_code == 200:
                logger.info("GET OK:%s?%s,response:%s\n", my_url, payload, resp.json())
                identify_code = resp.json().get('identify_code')
                if identify_code is None:
                    logger.error("GET ERROR:%s?%s,response:%s\n", my_url, payload, resp.json())
                    exit(1)
            else:
                logger.error("GET ERROR:%s?%s,response:%s\n", my_url, payload, resp.text)
                exit(1)

        # register
        try:
            my_url = URL + USERS + "/register"
            my_headers = {'content-type': 'application/json'}
            payload = dict()
            payload['account'] = '1234567' + rand_num
            payload['identify_code'] = identify_code
            payload['passwd'] = identify_code
            print "POST:%s?%s" % (my_url, payload)

            resp = requests.post(my_url, data=json.dumps(payload), headers=my_headers)
            logger.info("POST:%s?%s,response:%s\n", my_url, payload, resp.json())
        except Exception, e:
            logger.error("POST ERROR:%s?%s,error:%s\n", my_url, payload, e)
            exit(1)
        else:
            print 'resp:%s\n' % resp.text
            if resp.status_code == 200:
                logger.info("POST OK:%s?%s,head:%s,resp:%s\n", my_url, payload, my_headers, resp.json())
                user_id = resp.json().get('user_id')
                token = resp.json().get('token')
                if user_id is None or token is None:
                    logger.error("POST ERROR:%s?%s,head:%s,resp:%s\n", my_url, payload, my_headers, resp.json())
                    exit(1)
            else:
                logger.error("POST STATUS ERROR:%s?%s,head:%s,status:%d, resp:%s\n",
                             my_url, payload, my_headers, resp.status_code, resp.json())
                exit(1)

        # #####show user#########
        try:
            my_url = URL + USERS + "/users/" + user_id
            payload = dict()
            payload['token'] = token
            print "GET:%s?%s" % (my_url, payload)

            resp = requests.get(my_url, params=payload)
            logger.info("GET:%s?%s,response:%s\n", my_url, payload, resp.json())
        except Exception, e:
            logger.error("GET ERROR:%s?%s,error:%s\n", my_url, payload, e)
            exit(1)
        else:
            print 'resp:%s\n' % resp.text
            if resp.status_code == 200:
                logger.info("GET OK:%s?%s,response:%s\n", my_url, payload, resp.json())
                check_key = resp.json().get('account')
                if check_key is None:
                    logger.error("GET ERROR:%s?%s,response:%s\n", my_url, payload, resp.json())
                    exit(1)
            else:
                logger.error("GET ERROR:%s?%s,response:%s\n", my_url, payload, resp.text)
                exit(1)

        # #####user logout#########
        try:
            my_url = URL + USERS + "/logout/" + user_id
            payload = dict()
            payload['token'] = token
            print "GET:%s?%s" % (my_url, payload)

            resp = requests.get(my_url, params=payload)
            logger.info("GET:%s?%s,response:%s\n", my_url, payload, resp.json())
        except Exception, e:
            logger.error("GET ERROR:%s?%s,error:%s\n", my_url, payload, e)
            exit(1)
        else:
            print 'resp:%s\n' % resp.text
            if resp.status_code == 200:
                logger.info("GET OK:%s?%s,response:%s\n", my_url, payload, resp.json())
                check_key = resp.json().get('logout')
                if check_key is None:
                    logger.error("GET ERROR:%s?%s,response:%s\n", my_url, payload, resp.json())
                    exit(1)
            else:
                logger.error("GET ERROR:%s?%s,response:%s\n", my_url, payload, resp.text)
                exit(1)

        # #####user delete by self or admin, not test now#########

    # register one test account by admin, may login first?
    try:
        my_url = URL + ADMIN + "/add_user"
        my_headers = dict()
        my_headers['content-type'] = 'application/json'
        my_headers['token'] = 'this token is false'
        payload = dict()
        payload['account'] = '123456789'
        payload['passwd'] = '123456'
        # payload['token'] = 'this token is false'
        print "POST:%s?%s" % (my_url, payload)

        resp = requests.post(my_url, data=json.dumps(payload), headers=my_headers)
        logger.info("POST:%s?%s,response:%s\n", my_url, payload, resp.json())
    except Exception, e:
        logger.error("POST ERROR:%s?%s,error:%s\n", my_url, payload, e)
        exit(1)
    else:
        print 'resp:%s\n' % resp.text
        if resp.status_code == 200:
            logger.info("POST OK:%s?%s,head:%s,resp:%s\n", my_url, payload, my_headers, resp.json())
            user_id = resp.json().get('user_id')
            if user_id is None:
                logger.error("POST ERROR:%s?%s,head:%s,resp:%s\n", my_url, payload, my_headers, resp.json())
                exit(1)
        else:
            logger.error("POST STATUS ERROR:%s?%s,head:%s,status:%d, resp:%s\n",
                         my_url, payload, my_headers, resp.status_code, resp.json())
            exit(1)

    # #####user login#########
    try:
        my_url = URL + USERS + "/login"
        my_headers = {'content-type': 'application/json'}
        payload = dict()
        payload['account'] = '123456789'
        payload['passwd'] = '123456'
        print "POST:%s?%s" % (my_url, payload)

        resp = requests.post(my_url, data=json.dumps(payload), headers=my_headers)
        logger.info("POST:%s?%s,response:%s\n", my_url, payload, resp.json())
    except Exception, e:
        logger.error("POST ERROR:%s?%s,error:%s\n", my_url, payload, e)
        exit(1)
    else:
        print 'resp:%s\n' % resp.text
        if resp.status_code == 200:
            logger.info("POST OK:%s?%s,head:%s,resp:%s\n", my_url, payload, my_headers, resp.json())
            check_key = resp.json().get('user_id')
            new_token = resp.json().get('token')
            if check_key is None:
                logger.error("POST ERROR:%s?%s,head:%s,resp:%s\n", my_url, payload, my_headers, resp.json())
                exit(1)
        else:
            logger.error("POST STATUS ERROR:%s?%s,head:%s,status:%d, resp:%s\n",
                         my_url, payload, my_headers, resp.status_code, resp.json())
            exit(1)

    # #####show user#########
    try:
        my_url = URL + USERS + "/users/" + user_id
        rand_num = '123456789'
        payload = dict()
        payload['token'] = new_token
        print "GET:%s?%s" % (my_url, payload)

        resp = requests.get(my_url, params=payload)
        # logger.info("GET:%s?%s,response:%s\n", my_url, payload, resp.json())
    except Exception, e:
        logger.error("GET ERROR:%s?%s,error:%s\n", my_url, payload, e)
        exit(1)
    else:
        print 'resp:%s\n' % resp.text
        if resp.status_code == 200:
            logger.info("GET OK:%s?%s,response:%s\n", my_url, payload, resp.json())
            check_key = resp.json().get('account')
            if check_key is None:
                logger.error("GET ERROR:%s?%s,response:%s\n", my_url, payload, resp.json())
                exit(1)
        else:
            logger.error("GET ERROR:%s?%s,response:%s\n", my_url, payload, resp.text)
            exit(1)

    # #####user info modify#########
    try:
        my_url = URL + USERS + "/modify_user"
        my_headers = dict()
        my_headers['content-type'] = 'application/json'
        my_headers['token'] = new_token

        payload = dict()
        payload['user_name'] = 'jincm'
        payload['age'] = '78'
        payload['sex'] = 'm'
        payload['www'] = 'wwm'
        print "POST:%s?%s" % (my_url, payload)

        resp = requests.post(my_url, data=json.dumps(payload), headers=my_headers)
        # logger.info("POST:%s?%s,response:%s\n", my_url, payload, resp.json())
    except Exception, e:
        logger.error("POST ERROR:%s?%s,error:%s\n", my_url, payload, e)
        exit(1)
    else:
        print 'resp:%s\n' % resp.text
        if resp.status_code == 200:
            logger.info("POST OK:%s?%s,head:%s,resp:%s\n", my_url, payload, my_headers, resp.json())
            check_key = resp.json().get('modifyok')
            if check_key is None:
                logger.error("POST ERROR:%s?%s,head:%s,resp:%s\n", my_url, payload, my_headers, resp.json())
                exit(1)
        else:
            logger.error("POST STATUS ERROR:%s?%s,head:%s,status:%d, resp:%s\n",
                         my_url, payload, my_headers, resp.status_code, resp.json())
            exit(1)

    # #####upload user's head image#########
    try:
        my_url = URL + USERS + "/" + user_id + "/upload_head"
        payload = dict()
        payload['token'] = new_token
        # upload file
        file1 = '/home/jincm/zuohaoshi/server/test/1.png'
        file2 = '/home/jincm/zuohaoshi/server/test/2.jpg'
        myfiles = {'file1': open(file1, 'rb')}
        print "POST:%s?files:%s" % (my_url, myfiles)

        resp = requests.post(my_url, params=payload, files=myfiles)
    except Exception, e:
        logger.error("POST ERROR:%s?error:%s\n", my_url, e)
        exit(1)
    else:
        print 'resp:%s\n' % resp.text
        if resp.status_code == 200:
            logger.info("POST OK:%s?%s,resp:%s\n", my_url, payload, resp.json())
            check_key = resp.json().get('modifyok')
            if check_key is None:
                logger.error("POST ERROR:%s?head:%s,resp:%s\n", my_url, payload, resp.json())
                exit(1)
        else:
            logger.error("POST STATUS ERROR:%s?%s,status:%d, resp:%s\n",
                         my_url, payload, resp.status_code, resp.json())
            exit(1)

    # get user's posts

    # search one post filter by conditions

    print "###############################################"
    print "#######exit#############"
    print "###############################################"





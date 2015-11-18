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

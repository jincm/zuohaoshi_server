#!/usr/bin/env python
# encoding: utf-8
"""
    zuohaoshi application start app
    Good man is well
"""
import os
import sys
import time
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter

from flask import Flask
from flask import request,redirect,make_response,url_for,abort

app = Flask(__name__)
app.config.from_object("settings")

#init_db(app)

#To do:rename filename when file size larger 10M
file_handler = RotatingFileHandler(app.config['LOG_FILE'], 'a', 10*1024*1024, 10)
file_handler.setFormatter(Formatter('[%(thread)d %(filename)s %(lineno)d]%(asctime)s %(levelname)s: %(message)s'))
app.logger.addHandler(file_handler)
#debug
if app.config['LOG_INFO']:
    app.logger.setLevel(logging.INFO)
else:
    app.logger.setLevel(logging.WARN)
app.logger.info("test for app")

#import view and models
from myapp.view.admin import admin_blueprint
from myapp.view.users import users_blueprint
from myapp.view.activity import activity_blueprint
from myapp.view.group import group_blueprint

from myapp.models.user import *
from myapp.models.activity import *
from myapp.models.group import *

#register our blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(activity_blueprint)
app.register_blueprint(group_blueprint)
#app.register_blueprint(loster_blueprint)
#app.register_blueprint(message_blueprint)

#if __name__ == "__main__":
#    app.run(host=app.config.APP_HOST, port=app.config.APP_PORT, debug=app.debug)



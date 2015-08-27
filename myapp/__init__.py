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
app.config.from_object(config="settings")

init_db(app)

#debug
if not app.debug:
    #To do:rename filename when file size larger 10M
    file_handler = RotatingFileHandler(app.config['LOG_FILE'], 'a', 10*1024*1024, 10)
    file_handler.setLevel(logging.INFO) #app.config['LOG_LEVEL'])
    file_handler.setFormatter(Formatter('[%(filename)s %(lineno)d]%(asctime)s %(levelname)s: %(message)s'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

    app.logger.info("test for app")


from myapp.view.users import users_blueprint
from myapp.view.admin import admin_blueprint
from myapp.view.activity import activity_blueprint
from myapp.models.db import *

#register our blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(activity_blueprint)
#app.register_blueprint(group_blueprint, url_prefix='/group')
#app.register_blueprint(loster_blueprint, url_prefix='/loster')
#app.register_blueprint(message_blueprint, url_prefix='/message')

#if __name__ == "__main__":
#    app.run(host=app.config.APP_HOST, port=app.config.APP_PORT, debug=app.debug)



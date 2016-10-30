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
from flask.ext.login import LoginManager

################
# ## config ####
################
app = Flask(__name__)
app.config.from_object("settings")
# upload file max is 16M
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

####################
# ## extensions ####
####################
login_manager = LoginManager()
login_manager.init_app(app)

####################
# ## logging ####
####################
# To do:rename filename when file size larger 10M
file_handler = RotatingFileHandler(app.config['LOG_FILE'], 'a', 10*1024*1024, 10)
file_handler.setFormatter(Formatter('[%(process)d %(filename)s:%(lineno)d]%(asctime)s %(levelname)s: %(message)s'))
app.logger.addHandler(file_handler)
# debug
if app.config['LOG_INFO']:
    app.logger.setLevel(logging.INFO)
else:
    app.logger.setLevel(logging.WARN)
app.logger.info("test for app")

####################
# ## blueprints ####
####################
from myapp.view.admin import admin_blueprint
from myapp.view.users import users_blueprint
from myapp.view.activity import activity_blueprint
from myapp.view.group import group_blueprint
from myapp.view.message import message_blueprint

# register our blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(activity_blueprint)
app.register_blueprint(group_blueprint)
# app.register_blueprint(loster_blueprint)
app.register_blueprint(message_blueprint)

# app.logger.info("url is %s" % app.url_map)
# app.logger.info("functions is %s" % app.view_functions)

app.logger.info("end for register_blueprint")

from myapp.models.user import *
from myapp.models.activity import *
from myapp.models.group import *


####################
# ### flask-login ##
####################
@login_manager.request_loader
def load_user_from_request(request):
    app.logger.info("request:[%s],[%s],[%s]" % (request.headers, request.args, request.json))
    if request.args and "token" in request.args:
        token = request.args.get("token")
        #del request.args["token"]
    elif request.json and "token" in request.json:
        token = request.json.get("token")
        #del request.json["token"]
    elif request.headers and "token" in request.headers:
        token = request.headers.get("token")
        #del request.headers["token"]
    else:
        return None
    return User.get_user_from_token(token)

app.logger.debug("end for flask config and init\n")

########################
# ## error handlers ####
########################

# if __name__ == "__main__":
#     app.run(host=app.config.APP_HOST, port=app.config.APP_PORT, debug=app.debug)



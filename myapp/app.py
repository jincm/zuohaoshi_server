#!/usr/bin/env python
# coding = "utf-8"

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

from myapp.view.views import haoshi_v1_blueprint
from myapp.view.admin import admin_v1_blueprint
from myapp.models.db import *


def create_app(config="settings.py"):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_db(app)

    #register our blueprints
    app.register_blueprint(haoshi_v1_blueprint)
    app.register_blueprint(admin_v1_blueprint)
    #app.register_blueprint(activity_blueprint, url_prefix='/activity')
    #app.register_blueprint(group_blueprint, url_prefix='/group')
    #app.register_blueprint(loster_blueprint, url_prefix='/loster')
    #app.register_blueprint(message_blueprint, url_prefix='/message')

    return app

if __name__ == "__main__":
    app = create_app("settings.py")
    #debug
    if not app.debug:
        file_handler = RotatingFileHandler(app.config['LOG_FILE'])
        file_handler.setLevel(app.config[LOG_LEVEL])
        file_handler.setFormatter(Formatter('[%(filename)s %(lineno)d]%(asctime)s %(levelname)s: %(message)s'))
        app.logger.addHandler(file_handler)

    app.run(host='0.0.0.0', port=8000, debug=app.debug)


"""

#from werkzeug import security

@app.route('/')
def hello():
    print "hello world"

@app.route('/user/<username>')
def get_user(username):
    print "user is %s" % username

@app.route('/user/<int:userid>')
def get_user_id(userid):
    print "id is %d" % userid
    return redirect(url_for("login"))

@app.route('/user/', methods=['GET', 'POST'])
def user_test():
    app.logger.info("warning")
    app.logger.error("error done")
    print "test"

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['passwd']):
            return "logon"
        else:
            error = "Invalid username/passwd"
    else:
        keyword = request.args.get("username")

    return "200"
"""
"""
from flask import make_response
from flask import request


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


from myapp.db.database import db_session
from myapp.db.models import User

u = User('admin', 'admin@localhost')
db_session.add(u)
db_session.commit()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

"""
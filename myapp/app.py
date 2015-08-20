#!/usr/bin/env python
# coding = "utf-8"

"""
    zuohaoshi application start app
    Good man is well
"""

from flask import Flask
from flask import request,redirect,make_response,url_for
#from werkzeug import security

app = Flask(__name__)


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

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

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
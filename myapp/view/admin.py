# encoding: utf-8

"""
    zuohaoshi admin
    Be a good man
"""
from flask import Blueprint
from myapp import app

from myapp.models.user import User
from myapp.models.activity import Activity
from myapp.models.group import Group

admin_blueprint = Blueprint('admin', __name__, url_prefix='/v1/admin')

@admin_blueprint.route("/hello", methods=["GET", "POST"])
def hello():
    user = User()
    ac = Activity()
    group = Group()
    app.logger.info("Test for admin")
    return "hello admin"

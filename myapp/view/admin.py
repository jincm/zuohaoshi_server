# coding = utf-8
"""
    zuohaoshi admin
    Be a good man
"""
from flask import Blueprint
admin_blueprint = Blueprint('admin', __name__, url_prefix='/v1/admin')

@admin_blueprint.route("/hello", methods=["GET", "POST"])
def hello():
    print "hello admin"
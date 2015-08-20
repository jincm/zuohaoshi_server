# coding = utf-8
"""
    zuohaoshi admin
    Be a good man
"""
from flask import Blueprint
admin_v1_blueprint = Blueprint('admin', __name__, url_prefix='/v1/admin_manage')

@admin_v1_blueprint.route("/hello", methods=["GET", "POST"])
def hello():
    print "hello admin"
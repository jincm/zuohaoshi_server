from flask import Blueprint, request, abort

from myapp.models.group import Group
from myapp import app


group_blueprint = Blueprint('group', __name__, url_prefix='/v1/group')

#
#group_blueprint = Blueprint('group', __name__)
#loster_blueprint = Blueprint('loster', __name__)
#message_blueprint = Blueprint('message', __name__)

@group_blueprint.route('/<group>', methods=["GET"])
def show_group(group):
    group1 = Group()
    app.logger.info("Test for show_group")
    return 'Hello World! %s' % group
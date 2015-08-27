# coding = "utf-8"

"""
    zuohaoshi view
    Good man is well
"""

from flask import Blueprint, request, abort
from myapp.models.db import Haoshi_User

from myapp.app import app

users_blueprint = Blueprint('users', __name__, url_prefix='/v1/users')

#
#group_blueprint = Blueprint('group', __name__)
#loster_blueprint = Blueprint('loster', __name__)
#message_blueprint = Blueprint('message', __name__)

@users_blueprint.route('/<user>', methods=["GET"])
def show_user(user):
    user = Haoshi_User()
    user.get_user()
    app.logger.info("Test for show_user")
    return 'Hello World! %s' % user

@users_blueprint.route('/users', methods=['POST'])
def add_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or passwordi None:
        abort(400)
    user = Haoshi_User(username, password)
    user.hash_password(password)
    #user.save()

    return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}
#register

#login

#logout

#mongodb

#save file to oss
#post

#save redis

#relationship
#face_match



"""
@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})


@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})

if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(debug=True)
"""

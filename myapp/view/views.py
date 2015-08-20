# coding = "utf-8"

"""
    zuohaoshi view
    Good man is well
"""

from flask import Blueprint

haoshi_v1_blueprint = Blueprint('views', __name__, url_prefix='/v1/')

#activity_blueprint = Blueprint('activity', __name__)
#group_blueprint = Blueprint('group', __name__)
#loster_blueprint = Blueprint('loster', __name__)
#message_blueprint = Blueprint('message', __name__)

@haoshi_v1_blueprint.route('/<user>', methods=["GET"])
def show_user(user):
    return 'Hello World! %s' % user


#register

#mongodb

#login

#logout

#face_match


#save file to oss

#save redis

#relationship

#post


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

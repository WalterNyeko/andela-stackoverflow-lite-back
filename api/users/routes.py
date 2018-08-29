from flask import Blueprint, make_response, request, jsonify
from api.config import Configurations
from werkzeug.security import generate_password_hash, check_password_hash
from api.users.token import token_required
from api.users.models import User
from api.main.home import app
import datetime
import jwt

users = Blueprint('users', __name__)

config = Configurations()

@users.route('/api/v1/auth/signup', methods=['POST'])
@token_required
def SignUp(current_user):
    if not current_user.admin:
        return jsonify({'Message' : 'User does not have right to perform this operation'})
    input_data = request.get_json()
    password = generate_password_hash(input_data['password'], method='sha256')
    username = input_data['username']
    admin = False
    new_user = User()
    new_user.SignUp(username=username, password=password, admin=admin)
    return jsonify({'Message' : 'New User Created'})

@users.route('/api/v1/auth/login', methods=['GET'])
def LogIn():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify user', 404, {'WWW-Authentication' : 'Basic realm="Login Required"'})
    conn = config.connectToDB()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s;", auth.username)
    user = cur.fetchall()
    if not user:
        return make_response('Could not verify user', 404, {'WWW-Authentication' : 'Basic realm="Login Required"'})
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'Username' : auth.username, 'Exp' : datetime.datetime.utcnow()+ datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'Token' : token.decode('UTF-8')})
    return make_response('Could not verify user', 404, {'WWW-Authentication' : 'Basic realm="Login Required"'})

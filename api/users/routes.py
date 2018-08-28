from api.main.home import *
from api.config import *

users = Blueprint('users', __name__)

config = configurations()

@users.route('/api/v1/auth/signup', methods=['POST'])
@config.token_required
def SignUp(current_user):
    if not current_user.admin:
        return jsonify({'Message' : 'User does not have right to perform this operation'})
    input_data = request.get_json()
    hashed_password = generate_password_hash(input_data['password'], method='sha256')
    new_user = User(username = input_data['username'], password = hashed_password, admin = False)
    conn = config.connectToDB()
    cur = conn.cursor()
    cur.execute("INSERT INTO users(username, password, admin) VALUES (%s, %s, %s);", (new_user.username, new_user.password, new_user.admin))
    cur.commit()
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

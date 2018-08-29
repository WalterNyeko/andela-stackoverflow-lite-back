from api.config import Configurations
from flask import jsonify, request
from api.main.home import app
from functools import wraps
import jwt
config = Configurations()
def token_required(f):
    @wraps
    def decorated(*args, **kwargs):
        token = None
        if 'stackoverflow-lite' in request.headers:
            token = request.headers['stackoverflow-lite']
        if not token:
            return jsonify({'Message' : 'Token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            conn = config.connectToDB()
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username = %s;", data['username'])
            current_user = cur.fetchall()
        except:
            return jsonify({'Message' : 'Token is invalid'})
        return f(current_user, *args, **kwargs)
    return decorated
from flask import jsonify
from api.connectdb import Configurations

config = Configurations()

class Users():

    def signUp(self, username, email, password):
        sql = "INSERT INTO users(username, email, password) VALUES(%s, %s, %s)"
        sql_track = ""
        try:
            conn = config.connectToDB()
            cur = conn.cursor()
            cur.execute(sql, (username, email, password))
            conn.commit()
            return jsonify({'Message' : 'User successfully added to the database'})
        except:
            return jsonify({'Message' : 'User was not successfully added to the database'})
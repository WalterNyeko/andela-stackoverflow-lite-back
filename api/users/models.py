from flask import jsonify
from api.connectdb import Configurations

config = Configurations()

class Users():

    def signUp(self, username, email, password):
        sql = "INSERT INTO users(username, email, password) VALUES(%s, %s, %s)"
        try:
            conn = config.connectToDB()
            cur = conn.cursor()
            cur.execute(sql, (username, email, password))
            conn.commit()
            return jsonify({'Message' : 'User successfully added to the database'})
        except:
            return jsonify({'Message' : 'User was not successfully added to the database'})

    def checkuser(self,username):
        sql = "SELECT username FROM users WHERE username = %s"
        try:
            conn = config.connectToDB()
            cur = conn.cursor()
            cur.execute(sql, [username])
            conn.commit()
            theUser =cur.fetchone()
            return theUser
        except:
            return jsonify({'Message' : 'User was not retrived'})

    def checkPassword(self,password):
        sql = "SELECT password FROM users WHERE password = %s"
        try:
            conn = config.connectToDB()
            cur = conn.cursor()
            cur.execute(sql, [password])
            conn.commit()
            theUser =cur.fetchone()
            return theUser
        except:
            return jsonify({'Message' : 'Password was not retrived'})
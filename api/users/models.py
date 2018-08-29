from flask import jsonify
from api.config import Configurations

config = Configurations()

class User():
    # def __init__(self, username, password, admin):
    #     self.username = username
    #     self.password = password
    #     self.admin = admin

    def SignUp(self, username, password, admin):
        sql = "INSERT INTO users(username, password, admin) VALUES(%s, %s, %s)"
        try:
            conn = config.connectToDB()
            cur = conn.cursor()
            cur.execute(sql, (username, password, admin))
            conn.commit()
            return jsonify({'Message' : 'Question successfully added to the database'})
        except:
            return jsonify({'Message' : 'Question was not successfully added to the database'})
      



    
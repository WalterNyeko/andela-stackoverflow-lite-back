from flask import jsonify
from api.config import Configurations

config = Configurations()

class Question():
    # def __init__(self, question_title, question_body, question_votes, question_views, question_author, question_ask_date):
    #     self.question_title = question_title
    #     self.question_body = question_body
    #     self.question_votes = question_votes
    #     self.question_views = question_views
    #     self.question_author = question_author
    #     self.question_ask_date = question_ask_date

    def post_question(self, question_title, question_body, question_author):
        sql = "INSERT INTO questions(question_title, question_body, question_author) VALUES(%s, %s, %s)"
        try:
            conn = config.connectToDB()
            cur = conn.cursor()
            cur.execute(sql, (question_title, question_body, question_author))
            conn.commit()
            return jsonify({'Message' : 'Question successfully added to the database'})
        except:
            return jsonify({'Message' : 'Question was not successfully added to the database'})
            
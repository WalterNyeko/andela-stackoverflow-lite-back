from flask import jsonify
from api.config import Configurations

config = Configurations()

class Answer():
    # def __init__(self, answer_body, answer_author, answer_post_date, answer_status, answer_votes, question_id):
    #     self.answer_body = answer_body
    #     self.answer_author = answer_author
    #     self.answer_post_date = answer_post_date
    #     self.answer_status = answer_status
    #     self.answer_votes = answer_votes
    #     self.question_id = question_id
    def post_answer(self, answer_body, answer_author, question_id):
        sql = "INSERT INTO answers(answer_body, answer_author, question_id) VALUES(%s, %s, %s)"
        try:
            conn = config.connectToDB()
            cur = conn.cursor()
            cur.execute(sql, (answer_body, answer_author, question_id))
            conn.commit()
            return jsonify({'Message' : 'Answer successfully added to the database'})
        except:
            return jsonify({'Message' : 'Answer was not successfully added to the database'})
        

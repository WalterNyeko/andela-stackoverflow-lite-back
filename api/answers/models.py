from flask import jsonify
from api.connectdb import Configurations


config = Configurations()

class Answer():

    def post_answer(self, answer_body, answer_author, question_id):
        sql = "INSERT INTO answers(answer_body, answer_author, question_id) VALUES(%s, %s, %s)"
        try:

            conn = config.connectToDB()
            cur = conn.cursor()
            cur.execute(sql, (answer_body, answer_author, question_id))
            conn.commit()
            return {'Message' : 'Answer successfully added to the database'}
        except:
            return {'Message' : 'Answer was not successfully added to the database'}

    def delete_answer(self, question_id):
        sql = "DELETE FROM answers WHERE question_id = %s"
        try:
            conn = config.connectToDB()
            cur = conn.cursor()
            cur.execute(sql, [question_id])
            conn.commit()
            return jsonify({'Message' : 'Answer successfully deleted from the database'})
        except:
            return jsonify({'Message' : 'Answer was not successfully deleted from the database'})
    def accept_answer(self, answer_id):
        sql = "UPDATE answers SET answer_status = 1 WHERE answer_id=%s"
        try:
            conn = config.connectToDB()
            cur = conn.cursor()
            cur.execute(sql, [answer_id])
            conn.commit()
            return jsonify({'Message' : 'Answer successfully accepted'})
        except:
            return jsonify({'Message' : 'Answer was not successfully accepted'})

    def view_one_answer(self,answer_id):
        sql = "SELECT answer_status FROM answers WHERE answer_id = %s"
        try:
            conn = config.connectToDB()
            cur = conn.cursor()
            cur.execute(sql, [answer_id])
            conn.commit()
            theanswer =cur.fetchall()
            return theanswer
        except:
            return jsonify({'Message' : 'Answer was not retrived'})

    def view_all_answer(self,question_id):
        sql = "SELECT row_to_json(answers) FROM answers WHERE question_id = %s"
        try:
            conn = config.connectToDB()
            cur = conn.cursor()
            cur.execute(sql, [question_id])
            conn.commit()
            theanswer =cur.fetchall()
            return theanswer
        except:
            return jsonify({'Message' : 'Answer was not retrived'})

    def updateAnswer(self, answer_body, answer_id):
        sql = "UPDATE answers SET answer_body = %s WHERE answer_id = %s"
        try:
            conn = config.connectToDB()
            cur = conn.cursor()
            cur.execute(sql, [answer_body, answer_id])
            conn.commit()
        except:
            return jsonify({'Message': 'Update was unsuccessful'})

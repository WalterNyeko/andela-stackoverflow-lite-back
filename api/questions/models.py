from flask import jsonify
from api.connectdb import Configurations

config = Configurations()

class Question():

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

    def delete_question(self, question_id):
        sql = "DELETE FROM questions WHERE question_id = %s"
        try:
            conn = config.connectToDB()
            cur = conn.cursor()
            cur.execute(sql, [question_id])
            conn.commit()
            return jsonify({'Message' : 'Question successfully deleted from the database'})
        except:
            return jsonify({'Message' : 'Question was not successfully deleted from the database'})

    def view_all_questions(self):
        sql = "SELECT row_to_json(questions) FROM questions;"
        try:
            conn = config.connectToDB()
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            allquestions =cur.fetchall()
            return allquestions
        except:
            return jsonify({'Message' : 'Questions were not retrived'})

    def view_one_question(self,question_id):
        sql = "SELECT row_to_json(questions) FROM questions WHERE question_id = %s"
        try:
            conn = config.connectToDB()
            cur = conn.cursor()
            cur.execute(sql, [question_id])
            conn.commit()
            thequestion =cur.fetchall()
            return thequestion
        except:
            return jsonify({'Message' : 'Questions was not retrived'})

            
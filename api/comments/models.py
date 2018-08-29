from flask import jsonify
from api.config import Configurations

config = Configurations()

class Comments():
    # def __init__(self, comment_body, comment_author, comment_post_date,answer_id, question_id):
    #     self.comment_body = comment_body
    #     self.comment_author = comment_author
    #     self.comment_post_date = comment_post_date
    #     self.answer_id = answer_id
    #     self.question_id = question_id

    def post_comment(self, comment_body, comment_author, answer_id):
        sql = "INSERT INTO comments(comment_body, comment_author, answer_id) VALUES(%s, %s, %s)"
        try:
            conn = config.connectToDB()
            cur = conn.cursor()
            cur.execute(sql, (comment_body, comment_author, answer_id))
            conn.commit()
            return jsonify({'Message' : 'Comment successfully added to the database'})
        except:
            return jsonify({'Message' : 'Comment was not successfully added to the database'})
        
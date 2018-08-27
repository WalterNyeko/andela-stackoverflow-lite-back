from api.views import app

class User():
    def __init__(self, username, password, admin):
        self.username = username
        self.password = password
        self.admin = admin

class Question():
    def __init__(self, question_title, question_body, question_votes, question_views, question_author, question_ask_date):
        self.question_title = question_title
        self.question_body = question_body
        self.question_votes = question_votes
        self.question_views = question_views
        self.question_author = question_author
        self.question_ask_date = question_ask_date

class Answer():
    def __init__(self, answer_body, answer_author, answer_post_date, answer_status, answer_votes, question_id):
        self.answer_body = answer_body
        self.answer_author = answer_author
        self.answer_post_date = answer_post_date
        self.answer_status = answer_status
        self.answer_votes = answer_votes
        self.question_id = question_id

class Comments():
    def __init__(self, comment_body, comment_author, comment_post_date,answer_id, question_id):
        self.comment_body = comment_body
        self.comment_author = comment_author
        self.comment_post_date = comment_post_date
        self.answer_id = answer_id
        self.question_id = question_id
    
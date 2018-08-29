from flask import Flask, request, jsonify
from api.config import Configurations
from api.users.routes import users
from api.questions.routes import questions
from api.answers.routes import answers
from api.comments.routes import comments

config = Configurations()
config.create_tables

app = Flask(__name__)
app.register_blueprint(users)
app.register_blueprint(questions)
app.register_blueprint(answers)
app.register_blueprint(comments)


from flask import Flask, request, jsonify, make_response, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from api.answers.models import Answer
from api.comments.models import Comments
from api.questions.models import Question
from api.users.models import User
import datetime
import psycopg2
import psycopg2.extras
import jwt
from api.questions.routes import questions

blueprint = Blueprint()

app = Flask(__name__)
app.register_blueprint(questions)


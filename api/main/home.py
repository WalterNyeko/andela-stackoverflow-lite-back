from flask import Flask, request, jsonify, make_response, Blueprint
# from api.users.routes import users
from werkzeug.security import generate_password_hash, check_password_hash
from api.answers.models import Answer
from api.comments.models import Comments
from api.questions.models import Question
from api.users.models import User
import datetime
import psycopg2
import psycopg2.extras
import jwt
from api.config import configurations
from functools import wraps

config = configurations()
config.create_tables()

app = Flask(__name__)


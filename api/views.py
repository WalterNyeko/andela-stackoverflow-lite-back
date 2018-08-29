from flask import Flask, session, jsonify, request, json, Response, make_response
from api.questions.models import Question
from api.users.models import Users
from api.answers.models import Answer
import datetime
from werkzeug.security import check_password_hash
import jwt
from api.connectdb import Configurations
# from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'my-secret-keys-are-here'

config = Configurations()

questionObject = Question()
userObject = Users()
answerObject = Answer()

def token_required(f):
    # @wraps
    def decorated(*args, **kwargs):
        token = None
        if 'stackoverflow-lite' in request.headers:
            token = request.headers['stackoverflow-lite']
        if not token:
            return jsonify({'Message' : 'Token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            conn = config.connectToDB()
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username = %s AND password = %s;", (data['username'],data['password']) )
            current_user = cur.fetchone()
        except:
            return jsonify({'Message' : 'Token is invalid'})
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/api/v1/auth/signup', methods=['POST', 'GET'])
def SignUp():
    request_data  = request.get_json()
    if request_data['username'].strip() == "":
        return "Please fill in the username"
    else:
        username = request_data['username']
        
        email = request_data['email']
        password = request_data['password']
        userObject.signUp(username, email, password)
        return "User Created successfully"

@app.route('/api/v1/auth/login', methods=['GET'])
@token_required
def LogIn():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify user', 404, {'WWW-Authentication' : 'Basic realm="Login Required"'})
    conn = config.connectToDB()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s AND password= %s;", auth.password)
    user = cur.fetchall()
    if not user:
        return make_response('Could not verify user', 404, {'WWW-Authentication' : 'Basic realm="Login Required"'})
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'Username' : auth.username, 'Exp' : datetime.datetime.utcnow()+ datetime.timedelta(minutes=30)}, "Thisissecretkey")
        return jsonify({'Token' : token.decode('UTF-8')})
    return make_response('Could not verify user', 404, {'WWW-Authentication' : 'Basic realm="Login Required"'})

@app.route('/api/v1/questions', methods=['POST', 'GET'])
def postQuestion():
    request_data  = request.get_json()
    if request_data['question_title'].strip() == "":
        return "Please fill in the question title"
    else:
        question_title = request_data['question_title']
        question_body = request_data['question_body']
        question_author = request_data['question_author']
        questionObject.post_question(question_title, question_body, question_author)
        questions = questionObject.view_all_questions()
        return jsonify({'Message':questions}), 201

@app.route('/api/v1/question', methods=['GET'])
def getAllQuestions():
    questions = questionObject.view_all_questions()
    return jsonify({'Questions': questions}), 200

@app.route('/api/v1/questions/<int:question_id>', methods=['GET'])
def getOneQuestionById(question_id):
    question = questionObject.view_one_question(question_id=question_id)
    answers = answerObject.view_all_answer(question_id)
    return jsonify({'Questions': question, 'Answers' : answers})

@app.route('/api/v1/questions/<int:question_id>', methods=['DELETE'])
def DeleteQuestion(question_id):
    answerObject.delete_answer(question_id)
    questionObject.delete_question(question_id)
    return jsonify({'Questions' : 'Question Successfully Deleted'})
      
@app.route('/api/v1/questions/<int:question_id>/answers', methods=['POST'])
def postAnswer(question_id):
    request_data  = request.get_json()
    if request_data['answer_body'].strip() == "":
        return "Please fill in the answer"
    else:
        answer_body = request_data['answer_body']
        answer_author = request_data['answer_author']
        question_id = question_id
        answerObject.post_answer(answer_body, answer_author, question_id)
        return "Answer posted successfully"

@app.route('/api/v1/questions/<int:question_id>/answers/<int:answer_id>', methods=['PUT'])
def acceptAnswer(question_id, answer_id):
    theanswer = answerObject.view_one_answer(answer_id)
    if theanswer == 1:
        return "This Answer Is Already Accepted"
    else:
        answerObject.accept_answer(answer_id)
        return "Answer Accepted Successfully"


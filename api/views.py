from flask import Flask, session, jsonify, request, json, Response, make_response
from api.questions.models import Question
from api.users.models import Users
from api.answers.models import Answer
import datetime
from werkzeug.security import check_password_hash
from api.connectdb import Configurations
from validate_email import validate_email
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'somesecretstuffsforjwt'
jwt = JWTManager(app)

app.config['SECRET_KEY'] = 'my-secret-keys-are-here'

config = Configurations()

questionObject = Question()
userObject = Users()
answerObject = Answer()

@app.route('/api/v1/auth/signup', methods=['POST', 'GET'])
def SignUp():
    request_data  = request.get_json()
    if request_data['username'].strip() == "":
        return "Please fill in the username"
    else:
        username = request_data['username']
        email = request_data['email']
        password = request_data['password']
        is_valid = validate_email(email,verify=True)
        if (is_valid==True):

            conn = config.connectToDB()
            cur = conn.cursor()
            result = cur.execute("SELECT username from users WHERE username=%s", [username])
            if result is not None:
                return jsonify({'Message': 'User already exists'})
            else:   
                userObject.signUp(username, email, password)
                return jsonify({"Message":"User Created successfully"}), 201
        else:
            return jsonify({'Message': 'Wrong Email Detected'}), 400
        
        

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"Message": "No JSON format is provided"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"Message": "Username is missing"}), 400
    if username != 'test' and password != 'test':
        return jsonify({"Message": "Bad username or password"}), 401
    access_token = create_access_token(identity=username)
    return jsonify({"Messqge" : "Successfully Logged In", "Token" : access_token}), 200

@app.route('/api/v1/questions', methods=['POST', 'GET'])
@jwt_required
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
    return jsonify({'Questions': question, 'Answers' : answers}), 200

@app.route('/api/v1/questions/<int:question_id>', methods=['DELETE'])
@jwt_required
def DeleteQuestion(question_id):
    answerObject.delete_answer(question_id)
    questionObject.delete_question(question_id)
    return jsonify({'Questions' : 'Question Successfully Deleted'}), 202
      
@app.route('/api/v1/questions/<int:question_id>/answers', methods=['POST'])
@jwt_required
def postAnswer(question_id):
    request_data  = request.get_json()
    if request_data['answer_body'].strip() == "":
        return "Please fill in the answer"
    else:
        answer_body = request_data['answer_body']
        answer_author = request_data['answer_author']
        question_id = question_id
        answerObject.post_answer(answer_body, answer_author, question_id)
        return ({"Message": "Answer posted successfully"}), 201

@app.route('/api/v1/questions/<int:question_id>/answers/<int:answer_id>', methods=['PUT'])
@jwt_required
def acceptAnswer(question_id, answer_id):
    theanswer = answerObject.view_one_answer(answer_id)
    if theanswer == 1:
        return "This Answer Is Already Accepted"
    else:
        answerObject.accept_answer(answer_id)
        return jsonify({"Message": "Answer Accepted Successfully"}), 200


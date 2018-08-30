from flask import Flask, session, jsonify, request, json, Response, make_response
from api.questions.models import Question
from api.users.models import Users
from api.answers.models import Answer
import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from api.connectdb import Configurations
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import re
from flasgger import Swagger
from flasgger.utils import swag_from

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'somesecretstuffsforjwt'
jwt = JWTManager(app)

swagger = Swagger(app)

app.config['SECRET_KEY'] = 'my-secret-keys-are-here'

config = Configurations()

questionObject = Question()
userObject = Users()
answerObject = Answer()

@app.route('/api/v1/auth/signup', methods=['POST'])
@swag_from('swagger/signUp.yml')
def SignUp():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"Message": "No JSON format is provided"}), 400
        request_data  = request.get_json()
        if request_data['username'].strip() == "":
            return "Please fill in the username"
        else:
            username = request_data['username'].strip()
            email = request_data['email'].strip()
            password = request_data['password']
            if valid_email(email) == True:
                hashed_password = generate_password_hash(password)
                
                result = userObject.checkuser(username)
                if result is not None:
                    return jsonify({'Message': 'User already exists'})
                else:   
                    userObject.signUp(username, email, hashed_password)
                    return jsonify({"Message":"User Created successfully"}), 201
            else:
                return jsonify({'Message': 'Wrong Email Address'}), 400  
    else:
        return jsonify({'Message' : 'Wrong HTTP Request Method Detected'}), 400
@app.route('/api/v1/auth/login', methods=['POST'])
@swag_from('swagger/login.yml')
def login():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"Message": "No JSON format is provided"}), 400

        username = request.json.get('username', None).strip()
        password = request.json.get('password', None)
        if not username:
            return jsonify({"Message": "Username is missing"}), 400
        db_user = userObject.checkuser(username)
        db_pass = userObject.checkPassword(password)
    
        if username != db_user[0] or check_password_hash(password, db_pass[0]) !=True:
            return jsonify({"Message": "Invalid username or password"}), 401
        access_token = create_access_token(identity=username)
        return jsonify({"Messqge" : "Successfully Logged In", "Token" : access_token}), 200

    else:
        return jsonify({'Message' : 'Wrong HTTP Request Method Detected'}), 400    
@app.route('/api/v1/questions', methods=['POST'])
@swag_from('swagger/post_question.yml')
@jwt_required
def postQuestion():
    if request.method == 'POST':
        if not request.is_json:
                return jsonify({"Message": "Wrong JSON format is provided"}), 400
        request_data  = request.get_json()
        if request_data['question_title'].strip() == "":
            return "Please fill in the question title"
        else:
            question_title = request_data['question_title'].strip()
            question_body = request_data['question_body'].strip()
            current_user = get_jwt_identity()
        
            print(current_user)
            questionObject.post_question(question_title, question_body, current_user)
            return jsonify({'Message':'Question Posted Successfully'}), 201
    else:
        return jsonify({'Message' : 'Wrong HTTP Request Method Detected'}), 400
@app.route('/api/v1/questions', methods=['GET'])
@swag_from('swagger/view_questions.yml')
def getAllQuestions():
    questions = questionObject.view_all_questions()
    return jsonify({'Questions': questions}), 200

@app.route('/api/v1/questions/<int:question_id>', methods=['GET'])
@swag_from('swagger/view_one_question.yml')
def getOneQuestionById(question_id):
    question = questionObject.view_one_question(question_id=question_id)
    answers = answerObject.view_all_answer(question_id)
    if not question:
        return jsonify({'Message': 'No Question Found'}), 404
    else:
        return jsonify({'Question': question, 'Answers': answers}), 200

    

@app.route('/api/v1/questions/<int:question_id>', methods=['DELETE'])
@swag_from('swagger/delete_question.yml')
@jwt_required
def DeleteQuestion(question_id):
    author = questionObject.view_question_author(question_id)
    current_user = get_jwt_identity()
    if author[0] == current_user:
        answerObject.delete_answer(question_id)
        questionObject.delete_question(question_id)
        return jsonify({'Questions' : 'Question Successfully Deleted'}), 202
    else:
        return jsonify({'Message' : 'You are not the author of this question'}), 400
    
@app.route('/api/v1/questions/<int:question_id>/answers', methods=['POST'])
@swag_from('swagger/post_answer.yml')
@jwt_required
def postAnswer(question_id):
    request_data  = request.get_json()
    if request_data['answer_body'].strip() == "":
        return jsonify({"Message" : "Please fill in the answer"}), 400
    else:
        answer_body = request_data['answer_body'].strip()
        current_user = get_jwt_identity()
        question_id = question_id
        answerObject.post_answer(answer_body, current_user, question_id)
        result = questionObject.view_one_question_by_title('Why me?')
        print(result)
        return jsonify({"Message": "Answer posted successfully"}), 201

@app.route('/api/v1/questions/<int:question_id>/answers/<int:answer_id>', methods=['PUT'])
@swag_from('swagger/accept_answer.yml')
@jwt_required
def acceptAnswer(question_id, answer_id):
    if request.method == 'PUT':
        
        theanswer = answerObject.view_one_answer(answer_id)
        
        # request_data = request.get_json()
        # answer_body = request_data['answer_body'].strip()
        # answerObject.updateAnswer(answer_body, answer_id)
    
        if theanswer == 1:
            return jsonify({"Message" :"This Answer Is Already Accepted"}), 400
        else:
            answerObject.accept_answer(answer_id)
            return jsonify({"Message": "Answer Accepted Successfully"}), 200
    else:
        return jsonify({'Message': 'Wrong HTTP Request Method Detected'})
# def get_hashed_password(plain_text_password):
#     return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

# def check_password(plain_text_password, hashed_password):
#     return bcrypt.checkpw(plain_text_password, hashed_password)

def valid_email(email):
  return bool(re.match(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))
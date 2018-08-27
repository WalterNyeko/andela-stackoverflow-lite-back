from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from api.models import User, Question, Answer, Comments
from functools import wraps
import datetime
import psycopg2
import psycopg2.extras
import jwt

app = Flask(__name__)

app.config['SECRET_KEY'] == "ThisIsMySecretKey"

def connectToDB():
    connectionString = "dbname=andela user=root host=localhost password=mysql"
    try:
        return psycopg2.connect(connectionString)
    except:
        return jsonify({'Message' : 'Cannot connect to database'})

def token_required(f):
    @wraps
    def decorated(*args, **kwargs):
        token = None
        if 'stackoverflow-lite' in request.headers:
            token = request.headers['stackoverflow-lite']
        if not token:
            return jsonify({'Message' : 'Token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            conn = connectToDB()
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username = %s;", data['username'])
            current_user = cur.fetchall()
        except:
            return jsonify({'Message' : 'Token is invalid'})
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/api/v1/auth/signup', methods=['POST'])
@token_required
def SignUp(current_user):
    if not current_user.admin:
        return jsonify({'Message' : 'User does not have right to perform this operation'})
    input_data = request.get_json()
    hashed_password = generate_password_hash(input_data['password'], method='sha256')
    new_user = User(username = input_data['username'], password = hashed_password, admin = False)
    conn = connectToDB()
    cur = conn.cursor()
    cur.execute("INSERT INTO users(username, password, admin) VALUES (%s, %s, %s);", (new_user.username, new_user.password, new_user.admin))
    cur.commit()
    return jsonify({'Message' : 'New User Created'})

@app.route('/api/v1/auth/login', methods=['GET'])
def LogIn():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify user', 404, {'WWW-Authentication' : 'Basic realm="Login Required"'})
    conn = connectToDB()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s;", auth.username)
    user = cur.fetchall()
    if not user:
        return make_response('Could not verify user', 404, {'WWW-Authentication' : 'Basic realm="Login Required"'})
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'Username' : auth.username, 'Exp' : datetime.datetime.utcnow()+ datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'Token' : token.decode('UTF-8')})
    return make_response('Could not verify user', 404, {'WWW-Authentication' : 'Basic realm="Login Required"'})

@app.route('/api/v1/questions', methods=['GET'])
@token_required
def GetAllQuestions(current_user):
    if not current_user.admin:
        return jsonify({'Message' : 'User does not have right to perform this operation'})
    conn = connectToDB()
    cur = conn.cursor()
    cur.execute("SELECT * FROM questions;")
    questions = cur.fetchall()
    output_list = []
    for question in questions:
        question_data = {}
        question_data['question_id'] = question.question_id
        question_data['question_title'] = question.question_title
        question_data['question_body'] = question.question_body
        question_data['question_author'] = question.question_author
        question_data['question_ask_date'] = question.question_ask_date
        question_data['question_votes'] = question.question_votes
        question_data['question_views'] = question.question_views
        question_data['question_answers'] = question.question_answers
    output_list.append(question_data)
    return jsonify({'Questions' : output_list})

@app.route('/api/v1/questions/<int:question_id>', methods=['GET'])
@token_required
def GetOneQuestionById(current_user, question_id):
    if not current_user.admin:
        return jsonify({'Message' : 'User does not have right to perform this operation'})
    conn = connectToDB()
    cur = conn.cursor()
    cur.execute("SELECT * FROM questions WHERE question_id = %s;",question_id)
    question = cur.fetchall()
    if not question:
        return jsonify({'Message' : 'No Question Found For This ID'})
    else:
        question_data = {}
        question_data['question_id'] = question.question_id
        question_data['question_title'] = question.question_title
        question_data['question_body'] = question.question_body
        question_data['question_author'] = question.question_author
        question_data['question_ask_date'] = question.question_ask_date
        question_data['question_votes'] = question.question_votes
        question_data['question_views'] = question.question_views
        question_data['question_answers'] = question.question_answers
    return jsonify({'Questions' : question_data})

@app.route('/api/v1/questions/<int:question_title>', methods=['GET'])
@token_required
def GetOneQuestionByTitle(current_user, question_title):
    if not current_user.admin:
        return jsonify({'Message' : 'User does not have right to perform this operation'})
    conn = connectToDB()
    cur = conn.cursor()
    cur.execute("SELECT * FROM questions WHERE question_title = %s;",question_title)
    question = cur.fetchall()
    if not question:
        return jsonify({'Message' : 'No Question Found For This Title'})
    else:
        question_data = {}
        question_data['question_id'] = question.question_id
        question_data['question_title'] = question.question_title
        question_data['question_body'] = question.question_body
        question_data['question_author'] = question.question_author
        question_data['question_ask_date'] = question.question_ask_date
        question_data['question_votes'] = question.question_votes
        question_data['question_views'] = question.question_views
        question_data['question_answers'] = question.question_answers
    return jsonify({'Questions' : question_data})

@app.route('/api/v1/questions', methods=['POST'])
@token_required
def PostQuestion(current_user):
    if not current_user.admin:
        return jsonify({'Message' : 'User does not have right to perform this operation'})
    input_data = request.get_json()
    new_question = Question(question_title = input_data['question_title'],
    question_body = input_data['question_body'], question_author = input_data['question_author'], 
    question_ask_date = input_data['question_ask_date'], question_votes = 0, question_views = 0)
    conn = connectToDB()
    cur = conn.cursor()
    cur.execute("INSERT INTO questions(question_title, question_body, question_author, question_ask_date, question_votes, question_views) VALUES(%s, %s, %s, %s, %s, %s);",
    (new_question.question_title, new_question.question_body, new_question.question_author, new_question.question_ask_date, new_question.question_votes, new_question.question_views))
    conn.commit()
    return jsonify({'Message' : 'Question Posted Successfully'})

@app.route('/api/v1/questions/<int:question_id>', methods=['DELETE'])
@token_required
def DeleteQuestion(current_user, question_id):
    if not current_user.admin:
        return jsonify({'Message' : 'User does not have right to perform this operation'})
    conn = connectToDB()
    cur = conn.cursor()
    cur.execute("DELETE FROM questions WHERE question_id = %s;",question_id)
    question = cur.fetchall()
    if not question:
        return jsonify({'Message' : 'No Question Found For This ID'})
    else:
        conn.commit()
    return jsonify({'Questions' : 'Question Successfully Deleted'})

@app.route('/api/v1/questions/<int:question_id>/answers', methods=['POST'])
@token_required
def PostAnswer(current_user, question_id):
    if not current_user.admin:
        return jsonify({'Message' : 'User does not have right to perform this operation'})
    input_data = request.get_json()
    new_answer = Answer(answer_body = input_data['answer_body'],
    answer_author = input_data['answer_author'], answer_post_date = input_data['answer_post_date'], 
    answer_status = False,answer_votes=0, question_id = question_id)
    conn = connectToDB()
    cur = conn.cursor()
    cur.execute("INSERT INTO answers(answer_body, answer_author, answer_post_date, question_id) VALUES(%s, %s, %s, %s, %s, %s);",(new_answer.answer_body, new_answer.answer_author, 
    new_answer.answer_post_date, new_answer.question_id))
    conn.commit()
    return jsonify({'Message' : 'Answer Posted Successfully'})

@app.route('/api/v1/questions/<int:question_id>/answers/<int:answer_id>', methods=['PUT'])
@token_required
def AcceptOrEditAnswer(current_user, question_id, answer_id):
    if not current_user.admin:
        return jsonify({'Message' : 'User does not have right to perform this operation'})
    conn = connectToDB()
    cur = conn.cursor()
    cur.execute("SELECT * FROM answers WHERE answer_id = %s;",answer_id)
    answer = cur.fetchall()
    if not answer:
        return jsonify({'Message' : 'This Answer Is Not Found'})
    answer.answer_status = True
    conn.commit()
    return jsonify({'Message' : 'Answer Accepted Successfully'})

@app.route('/api/v1/questions/<int:question_id>/answers/<int:answer_id/comments>', methods=['PUT'])
@token_required
def CommentOnAnAnswer(current_user, question_id, answer_id):
    if not current_user.admin:
        return jsonify({'Message' : 'User does not have right to perform this operation'})
    input_data = request.get_json()
    new_comment = Comments(comment_body = input_data['comment_body'],
    comment_author = input_data['comment_author'], comment_post_date = input_data['comment_post_date'], 
    answer_id = answer_id, question_id = question_id)
    conn = connectToDB()
    cur = conn.cursor()
    cur.execute("INSERT INTO comments(comment_body, answer_author, comment_post_date, answer_id) VALUES(%s, %s, %s, %s);",(new_comment.comment_body, new_comment.comment_author, 
    new_comment.comment_post_date, new_comment.answer_id))
    conn.commit()
    return jsonify({'Message' : 'Comment Posted Successfully'})

@app.route('/api/v1/questions/<int:question_id>/answers/<int:answer_id>/<int:vote_value>', methods=['PUT'])
@token_required
def VoteForAnswer(current_user, question_id, answer_id, vote_value):
    if not current_user.admin:
        return jsonify({'Message' : 'User does not have right to perform this operation'})
    conn = connectToDB()
    cur = conn.cursor()
    cur.execute("SELECT * FROM answers WHERE answer_id = %s;",answer_id)
    answer = cur.fetchall()
    if not answer:
        return jsonify({'Message' : 'This Answer Is Not Found'})
    if vote_value == 1:
        answer.answer_vote = answer.answer_vote + 1
        conn.commit()
        return jsonify({'Message' : 'Answer UpVoted Successfully'})

    answer.answer_vote = answer.answer_vote - 1
    conn.commit()
    return jsonify({'Message' : 'Answer DownVoted Successfully'})


@app.route('/api/v1/questions/<string:question_author>', methods=['GET'])
@token_required
def FetchAllQuestionsAskedByAnAuthor(current_user, question_author):
    conn = connectToDB()
    cur = conn.cursor()
    cur.execute("SELECT * FROM questions WHERE question_author = %s;",question_author)
    questions = cur.fetchall()
    output_list = []
    for question in questions:
        question_data = {}
        question_data['question_id'] = question.question_id
        question_data['question_title'] = question.question_title
        question_data['question_body'] = question.question_body
        question_data['question_author'] = question.question_author
        question_data['question_ask_date'] = question.question_ask_date
        question_data['question_votes'] = question.question_votes
        question_data['question_views'] = question.question_views
        question_data['question_answers'] = question.question_answers
    output_list.append(question_data)
    return jsonify({'Questions' : output_list})

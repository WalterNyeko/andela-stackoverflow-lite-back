from api.main.home import *
from api.config import *

questions = Blueprint('questions', __name__)

@questions.route('/api/v1/questions', methods=['GET'])
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

@questions.route('/api/v1/questions/<int:question_id>', methods=['GET'])
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

@questions.route('/api/v1/questions/<int:question_title>', methods=['GET'])
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

@questions.route('/api/v1/questions', methods=['POST'])
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

@questions.route('/api/v1/questions/<int:question_id>', methods=['DELETE'])
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

@questions.route('/api/v1/questions/<string:question_author>', methods=['GET'])
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

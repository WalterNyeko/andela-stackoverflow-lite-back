
from flask import jsonify, request, Blueprint
from api.users.token import token_required
from api.config import Configurations
from api.answers.models import Answer


answers = Blueprint('answers',__name__)

config = Configurations()

@answers.route('/api/v1/questions/<int:question_id>/answers', methods=['POST'])
@token_required
def PostAnswer(current_user, question_id):
    if not current_user.admin:
        return jsonify({'Message' : 'User does not have right to perform this operation'})
    input_data = request.get_json()
    answer_body = input_data['answer_body']
    answer_author = input_data['answer_author']
    new_answer = Answer()
    new_answer.post_answer(answer_body=answer_body, answer_author=answer_author, question_id=question_id)
    return jsonify({'Message' : 'Answer Posted Successfully'})

@answers.route('/api/v1/questions/<int:question_id>/answers/<int:answer_id>', methods=['PUT'])
@token_required
def AcceptOrEditAnswer(current_user, question_id, answer_id):
    if not current_user.admin:
        return jsonify({'Message' : 'User does not have right to perform this operation'})
    conn = config.connectToDB()
    cur = conn.cursor()
    cur.execute("SELECT * FROM answers WHERE answer_id = %s;",answer_id)
    answer = cur.fetchall()
    if not answer:
        return jsonify({'Message' : 'This Answer Is Not Found'})
    answer.answer_status = True
    conn.commit()
    return jsonify({'Message' : 'Answer Accepted Successfully'})


@answers.route('/api/v1/questions/<int:question_id>/answers/<int:answer_id>/<int:vote_value>', methods=['PUT'])
@token_required
def VoteForAnswer(current_user, question_id, answer_id, vote_value):
    if not current_user.admin:
        return jsonify({'Message' : 'User does not have right to perform this operation'})
    conn = config.connectToDB()
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


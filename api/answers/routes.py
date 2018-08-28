
from api.main.home import *
from api.config import *

answers = Blueprint('answers',__name__)

@answers.route('/api/v1/questions/<int:question_id>/answers', methods=['POST'])
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

@answers.route('/api/v1/questions/<int:question_id>/answers/<int:answer_id>', methods=['PUT'])
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


@answers.route('/api/v1/questions/<int:question_id>/answers/<int:answer_id>/<int:vote_value>', methods=['PUT'])
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


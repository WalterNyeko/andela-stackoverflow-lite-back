from api.main.home import *
from api.config import *

comments = Blueprint('comments', __name__)

config = configurations()


@comments.route('/api/v1/questions/<int:question_id>/answers/<int:answer_id/comments>', methods=['PUT'])
@config.token_required
def CommentOnAnAnswer(current_user, question_id, answer_id):
    if not current_user.admin:
        return jsonify({'Message' : 'User does not have right to perform this operation'})
    input_data = request.get_json()
    new_comment = Comments(comment_body = input_data['comment_body'],
    comment_author = input_data['comment_author'], comment_post_date = input_data['comment_post_date'], 
    answer_id = answer_id, question_id = question_id)
    conn = config.connectToDB()
    cur = conn.cursor()
    cur.execute("INSERT INTO comments(comment_body, answer_author, comment_post_date, answer_id) VALUES(%s, %s, %s, %s);",(new_comment.comment_body, new_comment.comment_author, 
    new_comment.comment_post_date, new_comment.answer_id))
    conn.commit()
    return jsonify({'Message' : 'Comment Posted Successfully'})
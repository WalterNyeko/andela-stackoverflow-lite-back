from flask import request, jsonify, Blueprint
from api.users.token import token_required
from api.comments.models import Comments
from api.config import Configurations

config = Configurations()

comments = Blueprint('comments', __name__)

@comments.route('/api/v1/questions/<int:question_id>/answers/<int:answer_id/comments>', methods=['PUT'])
@token_required
def CommentOnAnAnswer(current_user, question_id, answer_id):
    if not current_user.admin:
        return jsonify({'Message' : 'User does not have right to perform this operation'})
    input_data = request.get_json()
    comment_author = input_data['comment_author']
    comment_body = input_data['comment_body']
    new_comment = Comments()
    new_comment.post_comment(comment_body=comment_body, comment_author=comment_author,answer_id=answer_id)
    return jsonify({'Message' : 'Comment Posted Successfully'})
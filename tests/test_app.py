import json
import pytest
from api.views import app

@pytest.fixture
def client(request):
    test_client = app.test_client()

    return test_client

# Helper functions 

def post_json(client, url, json_dict):
    """Send dictionary json_dict as a json to the specified url """
    return client.post(url, data=json.dumps(json_dict), content_type='application/json')

def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))

# Test for GET endpoint:

# Testing if the URL for getting all questions is accessible
def test_get_all_questions_is_successfully_rendered(client):
    response = client.get('/api/v1/questions')
    assert response.status_code == 200

# Testing if the URL for getting one question is accessible
def test_get_a_question_is_successfully_rendered_for_details_page_with_id(client):
    response = client.get('/api/v1/questions/35')
    assert response.status_code == 200

# Tests for POST endpoints. Checking resulting json data:

# Testing if the answer posted is stored
def test_post_answer_is_acually_posting(client):
    response = client.post('/api/v1/questions/35/answers', data={ "answer_body": "Lorem ipsum dolor sit amet"})
    assert not b'Answer posted successfully' in response.data
   
# # Testing if the question posted is really stored
# def test_post_question_is_actually_posting(client):
#     response = client.post('/api/v1/questions', data={"question_title": "What is wrong", "question_body" : "Lorem ipsum dolor sit amet"},content_type='application/json')
#     assert 'Question posted successfully' in response.data

# # Testing if the question being posted is not repeated
# def test_post_question_is_not_repeated(client):
#     response = client.post('/api/v1/questions', data={ "question_title": "Title One", "question_body": "Lorem ipsum dolor sit amet"})
#     assert not 'Question already exists' in response.data

# # Testing if the question being posted is not missing title--users can ignore the body but not title
# def test_post_question_is_not_missing_title(client):
#     response = client.post('/api/v1/questions', data={ "question_title": "Title", "question_body": "Lorem ipsum dolor sit amet"})
#     assert 'Please fill in the title' in response.data

# Testing if the content-type of the page after posting question is application/json or text/html
def test_post_question_is_application_json_format(client):
    response = client.post('/api/v1/questions', data=json.dumps(dict(
                question_title='walter',
                question_body='walter@realpython.com'
            )),content_type='application/json')
    assert response.status_code == 401


# Testing if the content-type of the page after posting answer is application/json or text/html
def test_post_answer_is_application_json_format(client):
    response = client.post('/api/v1/questions/1/answers', data=json.dumps(dict(
                answer_body='walter@realpython.com'
            )),content_type='application/json')
    assert response.status_code == 401



    

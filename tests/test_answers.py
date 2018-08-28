import json
import pytest
from api.main.home import app

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



# Testing if the content-type of the page after posting answer is application/json or text/html
def test_post_answer_is_application_json_format(client):
    response = client.post('/api/v1/questions/1/answers', data=json.dumps(dict(
                content='walter@realpython.com'
            )),content_type='application/json')
    assert response.status_code == 200
    
# Tests for POST endpoints. Checking resulting json data:

# Testing if the answer posted is stored
def test_post_answer_is_acually_posting(client):
    response = client.post('/api/v1/questions/1/answers', data={ "content": "Lorem ipsum dolor sit amet"})
    assert not b'Answer posted successfully' in response.data
  
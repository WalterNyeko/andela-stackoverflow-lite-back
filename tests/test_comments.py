import json
import pytest
from api.main.home import app
class my_tests:
    @pytest.fixture
    def client(self, request):
        test_client = app.test_client()

        return test_client

    # Helper functions 

    def post_json(self, client, url, json_dict):
        """Send dictionary json_dict as a json to the specified url """
        return client.post(url, data=json.dumps(json_dict), content_type='application/json')

    def json_of_response(self, response):
        """Decode json from response"""
        return json.loads(self.response.data.decode('utf8'))

    # Testing if the content-type of the page after posting comment is application/json or text/html
    def test_post_comment_is_application_json_format(self, client):
        self.response = client.post('/api/v1/questions/1/answers', data=json.dumps(dict(
                    content='walter@realpython.com'
                )),content_type='application/json')
        assert self.response.status_code == 200
        
    # Tests for POST endpoints. Checking resulting json data:

    # Testing if the comment posted is stored
    def test_post_comment_is_acually_posting(self, client):
        self.response = client.post('/api/v1/questions/1/answers/2/comments', data={ "content": "Lorem ipsum dolor sit amet"})
        assert not b'Answer posted successfully' in self.response.data
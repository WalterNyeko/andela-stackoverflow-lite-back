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

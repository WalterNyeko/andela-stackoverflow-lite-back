import json
import pytest
from api.views import app
from api.questions.models import Question

questionObject = Question()

@pytest.fixture
def client(request):
    test_client = app.test_client()

    return test_client

def test_view_question_response(client):
    pass

def test_user_does_not_exist(client):
    pass

def test_user_data_is_json_formatted(client):
    pass

def test_username_is_not_empty(client):
    pass

def test_if_dbConnection_is_established(client):
    pass
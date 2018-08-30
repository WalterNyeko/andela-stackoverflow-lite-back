import json
import pytest
from api.views import app
from api.connectdb import Configurations
from api.views import SignUp, valid_email
from api.questions.models import Question
from api.answers.models import Answer

config = Configurations()
questionObject = Question()
answerObject = Answer()



@pytest.fixture
def client(request):
    test_client = app.test_client()

    return test_client

def test_question_successfully_inserted_in_the_db(client):
    response = client.get('/api/v1/questions')
    assert response.status_code == 200

def test_if_deleted_question_is_completely_deleted(client):
    response = client.get('/api/v1/questions/7')
    assert response.status_code == 404


def test_if_dbConnection_is_established(client):
    connection = config.connectToDB()
    assert connection is not None



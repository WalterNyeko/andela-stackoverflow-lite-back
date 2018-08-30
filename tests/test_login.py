import json
import pytest
from api.views import app
from api.connectdb import Configurations
from api.views import SignUp, valid_email
from api.questions.models import Question
from api.answers.models import Answer
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask import request

config = Configurations()
questionObject = Question()
answerObject = Answer()



@pytest.fixture
def client(request):
    test_client = app.test_client()

    return test_client

def test_successfully_logged_in(client):
    response = client.get('/api/v1/auth/login')
    assert response.status_code == 201

def test_user_can_access_the_route(client):
    response = client.get('/api/v1/auth/login')
    assert response.status_code == 200


def test_if_dbConnection_is_established(client):
    connection = config.connectToDB()
    assert connection is not None

def test_user_provided_password(client):
    response = client.get('/api/v1/questions/7')
    assert response.status_code == 202

def test_user_gets_the_token(client):
    response = client.get('/api/v1/auth/login')
    data = request.getjson()
    username = data['username']
    access_token = create_access_token(identity=username)
    assert response.status_code == 200
    assert access_token is not None



import json
import pytest
from api.views import app
from api.users.models import Users

userObject = Users()

@pytest.fixture
def client(request):
    test_client = app.test_client()

    return test_client

def test_signUP_response(client):
    pass
    # data = { "username": "walter", "email": "email@gmail.com", "password": "1234"}
    # response = client.post('/api/v1/auth/signup', data)
    # userObject.signUp(data['username'],data['email'],data['password'])
    # assert response.status_code == 201

def test_user_does_not_exist(client):
    pass

def test_user_data_is_json_formatted(client):
    pass

def test_username_is_not_empty(client):
    pass

def test_if_dbConnection_is_established(client):
    pass


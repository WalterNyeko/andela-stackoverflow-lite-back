import json
import pytest
from api.views import app
from api.users.models import Users

userObject = Users()

@pytest.fixture
def client(request):
    test_client = app.test_client()

    return test_client

def test_login_succeeds_always(client):
    response = client.post('/api/v1/auth/login', data={ "username": "walter", "password": "walter456"})
    assert 'Successfully Logged In' in response.data

def test_user_does_not_exist(client):
    pass

def test_user_data_is_json_formatted(client):
    pass

def test_username_is_not_empty(client):
    pass

def test_if_dbConnection_is_established(client):
    pass
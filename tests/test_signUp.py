import json
import pytest
from api.views import app
from validate_email import validate_email
from api.connectdb import Configurations
from api.views import SignUp

config = Configurations()

@pytest.fixture
def client(request):
    test_client = app.test_client()

    return test_client

def test_user_does_not_exist_yet(client):
    conn = config.connectToDB()
    cur = conn.cursor()
    result = cur.execute("SELECT username from users WHERE username=%s", [SignUp.request_data['username']])
    assert result == False  

def test_username_is_not_empty(client):
    username = SignUp.request_data['username']
    assert username is not None

def test_if_dbConnection_is_established(client):
    connection = config.connectToDB()
    assert connection == True

def test_valid_email_provided(client):
    result = validate_email("nyekowalter69@gmail.com",verify=True)
    assert result == True


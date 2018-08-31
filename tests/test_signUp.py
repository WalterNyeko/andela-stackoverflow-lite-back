import json
import pytest
from api.views import app
from api.connectdb import Configurations
from api.views import SignUp, valid_email

config = Configurations()

@pytest.fixture
def client(request):
    test_client = app.test_client()

    return test_client

def test_user_does_not_exist_yet(client):
    conn = config.connectToDB()
    cur = conn.cursor()
    result = cur.execute("SELECT username from users WHERE username=%s", ["walter"])
    assert result == None 

def test_username_is_not_empty(client):
    username = client.post('/api/v1/auth/signup',data={'username':'walter'})
    assert username is not None

def test_if_dbConnection_is_established(client):
    connection = config.connectToDB()
    assert connection is not None

def test_valid_email_provided(client):
    result = valid_email("nyekowalter69@gmail.com")
    assert result is not None


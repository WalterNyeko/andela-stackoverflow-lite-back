from flask import Flask
from api.views import app
from api.connectdb import Configurations

config = Configurations()
# config.create_questions_table()
# config.create_users_table()
# config.create_answers_table()


if __name__ =='__main__':
    app.run(debug=True, port=8080)

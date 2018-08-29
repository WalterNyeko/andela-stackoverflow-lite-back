# StackOverflow-Lite
## Andela Challenge 3
[![Build Status](https://travis-ci.org/JSnakegitHub/Challenge-3.svg?branch=develop)](https://travis-ci.org/JSnakegitHub/Challenge-3)
[![Coverage Status](https://coveralls.io/repos/github/JSnakegitHub/Challenge-3/badge.svg?branch=develop)](https://coveralls.io/github/JSnakegitHub/Challenge-3?branch=develop)

## Installation Instructions for the app:
1. Install Flask using `pip install flask`
2. Clone the app using `git clone https://github.com/JSnakegitHub/Challenge-3.git`

## Getting Started With Tests:
### For Python 2:
1. `pip install pytest`
2. `pip install coverage report`
3. `pip install pytest-cov`
4. `pip install pytest-xdist`
### For Python 3:
1. `pip3 install pytest`
2. `pip3 install coverage report`
3. `pip3 install pytest-cov`
4. `pip3 install pytest-xdist`
## Running the tests on a virtual environment
### For python 2:
1. `pip install -U virtualenv`
2. `python -m virtualenv venv`
3. `source venv/bin/activate` # in Windows -> venv\Scripts\activate.bat
4. `pip install pytest`
### For Python 3:
1. `pip3 install -U virtualenv`
2. `python3 -m virtualenv venv`
3. `source venv/bin/activate` # in Windows -> venv\Scripts\activate.bat
4. `pip install pytest`
### For Python 3.6+:
2. `python3 -m venv venv`
3. `source venv/bin/activate` # in Windows -> venv\Scripts\activate.bat
4. `pip install pytest`
### What The Tests Are Testing:
1. If the required endpoints are rendered.
2. If the requests are being sent in the right format (JSON-JavaScript Object Notation).
3. If Validations are being respected

## Testing the App Locally.
1. [Postman](https://www.getpostman.com/) should be used to test the application locally
2. Move to the project directory locally
3. Once you are in the project's root directory, run the command `python run.py`.
4. At this point the server should be running.
5. The application is set to run on port 8080 

|URL for the route| Function Performed by the route| HTTP Method|
|-----------------|--------------------------------|-------------|
|`127.0.0.1:8080/api/v1/questions`| Retrive all questions|`GET`|
|`127.0.0.1:8080/api/v1/questions`|Post a question|`POST`|
|`127.0.0.1:8080/api/v1/questions/question_id`|Retrieve Question of a particular ID|`GET`|
|`127.0.0.1:8080/api/v1/questions/question_id/answers`|Post Answers to Question of a given ID|`POST`|
|`127.0.0.1:8080/api/v1/questions/question_id`|Deletes a question|`DELETE`|
|`127.0.0.1:8080/api/v1/questions/question_id/answers/answer_id`|Accept/Edit an answer|`PUT`|
|`127.0.0.1:8080/api/v1/auth/signup`|Register User|`POST`|
|`127.0.0.1:8080/api/v1/auth/login`|Login User|`GET`|

## Deployment
1. The app can be deplyed on Heroku following the Heroku [Documentation](https://devcenter.heroku.com/categories/reference).

## Contributing
Contributions for this project is allowed.
## Versioning
GitHub was used to help track the different versions of the project. 

## Authors
1. Walter Nyeko, under supervision of Hadijah Kyampeire
## License
1. This project is licensed under the Andela License


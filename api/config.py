from api.main.home import *

class configurations:
    def secrete_key(self):
        app.config['SECRET_KEY'] == "ThisIsMySecretKey"
        return app.config['SECRET_KEY']


    def connectToDB(self):
        connectionString = "dbname=andela user=postgres host=localhost"
        try:
            return psycopg2.connect(connectionString)
        except:
            return jsonify({'Message' : 'Cannot connect to database'})

    def token_required(self,f):
        @wraps
        def decorated(*args, **kwargs):
            token = None
            if 'stackoverflow-lite' in request.headers:
                token = request.headers['stackoverflow-lite']
            if not token:
                return jsonify({'Message' : 'Token is missing'})
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
                conn = self.connectToDB()
                cur = conn.cursor()
                cur.execute("SELECT * FROM users WHERE username = %s;", data['username'])
                current_user = cur.fetchall()
            except:
                return jsonify({'Message' : 'Token is invalid'})
            return f(current_user, *args, **kwargs)
        return decorated

    def create_tables(self):
        sqlcommandforQuestions =(
            """
            CREATE TABLE IF NOT EXISTS questions(question_id SERIAL PRIMARY KEY, question_title VARCHAR(250),
             question_body VARCHAR(250), question_votes INT(12), question_views INT(10), question_author VARCHAR(100),
              question_ask_date TIMESTAMP)
            """
        )

        sqlcommandforAnswers =(
            """
            CREATE TABLE IF NOT EXISTS answers(answer_id SERIAL PRIMARY KEY,
             answer_body VARCHAR(250), answer_author VARCHAR(100),
              answer_post_date TIMESTAMP, answer_votes INT(12), answer_status INT(2), question_id INT(12))
            """
        )

        sqlcommandforComments =(
            """
            CREATE TABLE IF NOT EXISTS comments(comment_id SERIAL PRIMARY KEY,
             comment_body VARCHAR(250), comment_author VARCHAR(100),
              comment_post_date TIMESTAMP, answer_id INT(12), question_id INT(12))
            """
        )

        sqlcommandforUsers =(
            """
            CREATE TABLE IF NOT EXISTS users(user_id SERIAL PRIMARY KEY,
             username VARCHAR(250), password VARCHAR(100),
             admin INT(2))
            """
        )
        conn = self.connectToDB()
        self.cur = conn.cursor()
        self.cur.execute(sqlcommandforQuestions)
        conn.commit()
        self.cur.execute(sqlcommandforAnswers)
        conn.commit()
        self.cur.execute(sqlcommandforComments)
        conn.commit()
        self.cur.execute(sqlcommandforUsers)
        conn.commit()
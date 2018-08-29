from api.main.home import app
from flask import jsonify
import psycopg2


class Configurations:

    def connectToDB(self):
        connectionString = "dbname=stackoverflow user=postgres host=localhost port=5432"
        try:
            psycopg2.connect(connectionString)
            print("Connection established")
            return jsonify({'Message' : 'Connected to database'})
        except:
            return jsonify({'Message' : 'Cannot connect to database'})

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
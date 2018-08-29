from flask import jsonify
import psycopg2


class Configurations:

    def connectToDB(self):
        connectionString = "dbname='stackoverflow' user='postgres' password='1234' host='localhost' port='5432'"
        try:
            self.conn = psycopg2.connect(connectionString)
            print("Connection established")
            return self.conn
            
        except:
            print('Cannot connect to database')
            return jsonify({'Message' : 'Cannot connect to database'})

    def create_questions_table(self):
        sqlcommandforQuestions =(
            """
            CREATE TABLE IF NOT EXISTS questions(question_id SERIAL PRIMARY KEY, question_title VARCHAR(250),
             question_body VARCHAR(250), question_author VARCHAR(100),
              question_ask_date TIMESTAMP)
            """
        )
        self.conn = self.connectToDB()
        self.cur = self.conn.cursor()
        self.cur.execute(sqlcommandforQuestions)
        self.conn.commit()
    
    
    def create_users_table(self):
        sqlcommandforUsers =(
            """
            CREATE TABLE IF NOT EXISTS users(user_id SERIAL PRIMARY KEY, username VARCHAR(250),
             email VARCHAR(250), password VARCHAR(100), admin smallint)
            """
        )
        self.conn = self.connectToDB()
        self.cur = self.conn.cursor()
        self.cur.execute(sqlcommandforUsers)
        self.conn.commit()
    
    def create_answers_table(self):
        sqlcommandforAnswers =(
            """
            CREATE TABLE IF NOT EXISTS answers(answer_id SERIAL PRIMARY KEY, answer_body VARCHAR(250),
             answer_author VARCHAR(250), answer_status smallint, answer_votes INTEGER, question_id INTEGER,
             FOREIGN KEY (question_id) REFERENCES questions(question_id))
            """
        )
        self.conn = self.connectToDB()
        self.cur = self.conn.cursor()
        self.cur.execute(sqlcommandforAnswers)
        self.conn.commit()
    
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
        DB_USER = os.getenv('DB_USER', 'postgres')
        DB_PASSWORD = os.getenv('DB_PASSWORD', '134256')
        DB_NAME = os.getenv('DB_NAME', 'trivia_test')
        self.database_path = "postgres://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    def test_get_paginated_questions(self):
        response = self.client().get('/questions')
        json_data = json.loads(response.data)

        self.assertEqual(200, response.status_code)
        self.assertTrue(json_data['success'])
        self.assertTrue(json_data['total_questions'])
        self.assertTrue(json_data['questions'])
        self.assertTrue(json_data['categories'])


    def test_404_sent_requesting_questions_beyond_valid_page(self):
        response = self.client().get('/questions?page=1000')
        json_data = json.loads(response.data)

        self.assertEqual(404, response.status_code)
        self.assertFalse(json_data['success'])
        self.assertEqual("resource not found", json_data['message'])


    def test_get_categories(self):
        response = self.client().get('/categories')
        json_data = json.loads(response.data)

        self.assertEqual(200, response.status_code)
        self.assertTrue(json_data['success'])
        self.assertTrue(json_data['categories'])


    def test_404_sent_requesting_non_existing_category(self):
        response = self.client().get('/categories/7777')
        json_data = json.loads(response.data)

        self.assertEqual(404, response.status_code)
        self.assertFalse(json_data['success'])
        self.assertEqual("resource not found", json_data['message'])


    def test_delete_question(self):
        question = Question(question='Who i am?', answer='my name is aamad naseem abbasi.',
                            difficulty=1, category=1)
        question.insert()
        question_id = question.id

        response = self.client().delete(f'/questions/{question_id}')
        json_data = json.loads(response.data)

        question = Question.query.filter(Question.id == question.id).one_or_none()

        self.assertEqual(200, response.status_code)
        self.assertTrue(json_data['success'])
        self.assertEqual(str(question_id), json_data['deleted'])
        self.assertIsNone(question)


    def test_422_sent_deleting_non_existing_question(self):
        response = self.client().delete('/questions/yu')
        json_data = json.loads(response.data)

        self.assertEqual(422, response.status_code)
        self.assertFalse(json_data['success'])
        self.assertEqual("unprocessable", json_data['message'])


    def test_add_question(self):
        new_question = {
            'question': 'how are you?',
            'answer': 'i am fine',
            'difficulty': 4,
            'category': 2
        }
        initial_question_count = len(Question.query.all())
        response = self.client().post('/questions', json=new_question)
        json_data = json.loads(response.data)
        final_question_count = len(Question.query.all())

        self.assertEqual(200, response.status_code)
        self.assertTrue(json_data["success"])
        self.assertEqual(initial_question_count + 1, final_question_count)



    def test_422_add_question(self):
        new_question = {
            'question': 'how are you?',
            'answer': 'i am fine',
            'difficulty': '',
            'category': 1
        }
        res = self.client().post('/questions', json=new_question)
        json_data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(json_data["success"], False)
        self.assertEqual(json_data["message"], "unprocessable")

    def test_search_questions(self):
        new_search = {'searchTerm': 'ammad'}
        res = self.client().post('/questions/search', json=new_search)
        json_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data['success'], True)
        self.assertIsNotNone(json_data['questions'])
        self.assertIsNotNone(json_data['total_questions'])

    def test_404_search_question(self):
        new_search = {
            'searchTerm': '',
        }
        res = self.client().post('/questions/search', json=new_search)
        json_data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(json_data["success"], False)
        self.assertEqual(json_data["message"], "resource not found")

    def test_get_questions_per_category(self):
        res = self.client().get('/categories/1/questions')
        json_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data['success'], True)
        self.assertTrue(len(json_data['questions']))
        self.assertTrue(json_data['total_questions'])
        self.assertTrue(json_data['current_category'])

    def test_404_get_questions_per_category(self):
        res = self.client().get('/categories/a/questions')
        json_data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(json_data["success"], False)
        self.assertEqual(json_data["message"], "resource not found")

    def test_play_quiz(self):
        new_quiz_round = {'previous_questions': [],'quiz_category': {'type': 'Entertainment', 'id': 5}}

        res = self.client().post('/quizzes', json=new_quiz_round)
        json_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data['success'], True)

    def test_404_play_quiz(self):
        new_quiz_round = {'previous_questions': []}
        res = self.client().post('/quizzes', json=new_quiz_round)
        json_data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(json_data["success"], False)
        self.assertEqual(json_data["message"], "unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
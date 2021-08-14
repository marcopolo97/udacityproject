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
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
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
# Test for getting questions

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))


    def test_404__requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

## Tests for searhing for a term

def test_search_for_question(self):

    new_searchTERM = {
        "searchTerm": "Tom"
        }
    res = self.client().post('/search', json=new_searchTERM)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertIsNotNone(data['questions'])

def test_error_search_question(self):

    new_searchTERM = {
        "searchTerm": "something here"
        }
    res = self.client().post('/search', json=new_search)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'not found')

## Tests for creating a question

def test_create_question(self):
    new_question = {
        "question": "What sport does Stephen Curry play?",
        "answer": "Basketball",
        "difficulty": "4"
    }

    res = self.client().post('/add', json=self.new_question)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['created'])
    self.assertTrue(len(data['question']))


def test_error_when_creating_question(self):
    new_question_error = {
        "question": "",
        "answer": "",
        "difficulty": ""
    }
    res = self.client().post('/add', json=self.new_question_error)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 400)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'bad request')

# Tests for deleting a question

def test_delete_question(self):
    res = self.client().delete('/questions/2')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['deleted_question']['id'], 2)


def test_422_if_question_does_not_exist(self):
    res = self.client().delete('/questions/1000')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'not found')

## Tests for getting questions for each category

def test_questions_by_a_category(self):

    res = self.client().get('/categories/2/questions')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['totalQuestions'], 3)

def test_error_questions_by_a_category(self):

    res = self.client().get('/categories/95/questions')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 422)
    self.assertEqual(data['success'], False)


## Tests for starting the quiz 

def test_for_quiz(self):

    res = self.client().post('/quizzes', json={
        'previous_questions': [9],
        'quiz_category': {'id': 4, 'type': 'History'}
        })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertIsNotNone(data['question'])

def test_error_for_quiz(self):
    res = self.client().post('/quizzes', json={
        'previous_questions': [],
        'quiz_category': {'id': 1}
        })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 422)
    self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

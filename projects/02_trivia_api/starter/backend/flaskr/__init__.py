import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={"*": {"origins": "*"}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def categories():
    return jsonify({
      'success' : True,
      'categories': theCategories()
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 


  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

    '''Function to get the categories '''
  
  def theCategories():
    categories = {}
    for category in Category.query.all():
      categories[category.id] = category.type
    
    return categories

  @app.route('/questions')
  def get_questions():
    all_questions = Question.query.all()
    current_questions = paginate_questions(request, all_questions)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(all_questions),
      'categories': theCategories(),
      'current_category': None
    })
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()
      all_questions = Question.query.all()

      current_questions = paginate_questions(request, all_questions)

      return jsonify({
        'success': True,
        'deleted': question_id,
        'questions': current_questions,
        'total_questions': len(all_questions)
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/add', methods=['GET','POST'])
  def add_question():

    body = request.get_json()
    
    try:
      new_question = body.get('question')
      new_answer = body.get('answer')
      new_category = body.get('category')
      new_difficulty = body.get('difficulty')

      question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
      
      question.insert()

      all_questions = Question.query.all()

      current_questions = paginate_questions(request, all_questions)

      return jsonify({
        'success': True,
        'question': new_question,
        'answer': new_answer,
        'category': new_category,
        'difficulty': new_difficulty
      })

    except Exception as e:
 
      print('Exception is >> ',e )
 
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 

'''

  @app.route('/search', methods=['POST'])

  def search_question():
  
    body = request.get_json()
  
    try:
    
      search_term = body.get('searchTerm') 

      returning_search_term = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

      format_these_questions = paginate_questions(request, returning_search_term)

      return jsonify({
        'status': True,
        'questions': format_these_questions,
        'total_questions': len(Question.query.all()),
        'current_category': None
      })
    
    except Exception as e:
    
      print('Exception is >> ',e )
    
      abort(422)




  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:id>/questions')
  def getByCategory(id):

    try:
      
      this_category = Category.query.filter_by(id=id).one_or_none()
      
      questions = Question.query.filter_by(category = str(id)).all()
      
      format_these_questions = paginate_questions(request, questions)

      return jsonify({
        'status': True,
        'questions': format_these_questions,
        'total_questions': len(questions),
        'current_category': this_category.type
      })
    except Exception as e:
    
      print('Exception is >> ',e )
    
      abort(422)


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404
        
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "This is unprocessable"
        }), 422
  
  return app

    
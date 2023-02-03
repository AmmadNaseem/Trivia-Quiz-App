from itertools import islice
import os
from flask import Flask, make_response, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def requested_header(response):
        response.headers.add('Access-Control-Allow-Headers',
                            'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                            'GET,PUT,POST,DELETE,OPTIONS')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.type).all()

        if len(categories) == 0:
            abort(404)
        
        categories_list = {}
        for category in categories:
            categories_list[category.id] = category.type


        return jsonify({
            'success': True,
            'categories':categories_list 
        })


    """FOR PAGINATION OF QUESTIONS====="""
    def paginate_questions(request, selection):
       page = request.args.get('page', 1, type=int)
       start = (page - 1) * QUESTIONS_PER_PAGE
       end = start + QUESTIONS_PER_PAGE

       current_questions = list(islice(
            (question.format() for question in selection), start, end
       ))

       return current_questions

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    """
    @app.route('/questions')
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        categories = Category.query.order_by(Category.type).all()

        if len(current_questions) == 0:
            abort(404)

        categories_list = {}
        for category in categories:
            categories_list[category.id] = category.type


        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': categories_list,
            'current_category': None
        })

    """
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    """
    @app.route("/questions/<question_id>", methods=['DELETE'])
    def delete_question(question_id):
        try:
            question=Question.query.filter(Question.id==question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)


            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(selection),
            })

        except:
            abort(422)


    """
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score."""
    @app.route("/questions", methods=['POST'])
    def insert_question():
        body = request.get_json()
        
        if (body.get('question') is None or body.get('answer') is None or body.get('difficulty') is None or body.get('category') is None):
            response = jsonify({
                'success': False,
                'error': 'Bad Request',
                'message': 'question, answer, difficulty, and category are required fields'
            })
            abort(make_response(response, 422))

        else:    
            new_question = body.get('question')
            new_answer = body.get('answer')
            new_difficulty = body.get('difficulty')
            new_category = body.get('category')
            try:
                question = Question(question=new_question, answer=new_answer,difficulty=new_difficulty, category=new_category)
                question.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                    'success': True,
                    'created': question.id,
                    'questions': current_questions,
                    'total_questions': len(selection),
                })

            except:
                abort(422)


    """
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question."""
    @app.route('/questions/search', methods=['POST'])
    def find_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', None)

        if search_term:
            selection=Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search_term)))
            current_questions=paginate_questions(request,selection)

            
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection.all()),
                'current_category': None
            })
        abort(404)

    """
    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
    
        try:
            selection = Question.query.filter_by(category=str(category_id)).all()
            current_questions=paginate_questions(request,selection)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'current_category': category_id
            })
        except:
            abort(422)
          

    """"
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            body = request.get_json()
            if (body.get('quiz_category') is None or body.get('previous_questions') is None):
                response=jsonify({
                    'success': False,
                    'error': 'Bad Request',
                    'message': 'quiz category and previous questions are required fields'
                })
                abort(make_response(response, 422))
            

            category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')
           
            
            if category['type'] == 'click':
                available_questions = [question for question in Question.query.all() if question.id not in previous_questions]

            else:
                available_questions = [question for question in Question.query.filter_by(category=category['id']).all() if question.id not in previous_questions]


            new_question = random.choice(available_questions).format() if available_questions else None


            return jsonify({
                'success': True,
                'question': new_question
            })
            


        except:
            abort(422)

    """"
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400


    return app


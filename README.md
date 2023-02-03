# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.


# Trivia Project Documentation

Trivia is a quiz type app that ask questions to user and user will give answer or can show answer. Also user can play game.
This app includes following features:

1- Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.

2- Delete questions.

3- Add questions and require that they include question and answer text.

4- Search for questions based on a text query string.

5- Play the quiz game, randomizing either all questions or within a specific category.

All backend code follows PEP8 style guidelines.
Student Guidelines <br/>
These are the steps for successfuly run or install project in PC.<br/>


# Getting Started
Pre-requisites and Local Development

Developers using this project should already have Python3, pip and node installed on their local machines.
### Backend

From the backend folder run pip install updatedRequirements.txt. All required packages are included in the requirements file.

To run the application run the following commands:

export FLASK_APP=flaskr <br/>
export FLASK_ENV=development <br/>
flask run <br/>

These commands put the application in development and directs our application to use the __init__.py file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the Flask documentation.

The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.
### Frontend

From the frontend folder, run the following commands to start the client:

npm install <br/>
npm start <br/>

By default, the frontend will run on http://127.0.0.1:3000.
# Tests

In order to run tests  and apis navigate to the backend folder and install database for api and tests:
install psql (pgadmin4)
create new trivia_test
create new trivia_test
copy script from Database folder and run the script in query tool of pgAdmin4. 
python test_flaskr.py

The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.
# API Reference
Getting Started

    Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
    Authentication: This version of the application does not require authentication or API keys.

# Error Handling

Errors are returned as JSON objects in the following format:

	 {
    "success": False, 
    "error": 400,
    "message": "bad request"
   }
	 
	 

 ## The API will return three error types when requests fail:

    400: Bad Request
    404: Resource Not Found
    422: Not Processable


### Expected endpoints and behaviors

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.

Sample: `curl http://127.0.0.1:5000/categories`
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

---

`GET '/questions?page=${integer}'`

- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: `page` - integer <br/>
Sample:`curl -X GET	 http://127.0.0.1:5000/page=1`

- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
    }
  ],
  "totalQuestions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "History"
}
```

---

`GET '/categories/${id}/questions'`

- Fetches questions for a cateogry specified by id request argument
- Request Arguments: `id` - integer <br/>
Sample: `curl http://127.0.0.1:5000/categories/3/questions`
- Returns: An object with questions for the specified category, total questions, and current category string

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 4
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "History"
}
```

---

`DELETE '/questions/${id}'`

- Deletes a specified question using the id of the question
- Request Arguments: `id` - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.

Sample:`curl -X DELETE http://127.0.0.1:5000/questions/16`

```json
{
  "success": true
}
```
---

`POST '/quizzes'`

- Sends a post request in order to get the next question <br/>
Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"type":"Geography","id":"3"}, "previous_questions":[13]}'`
- Request Body:

```json
{
    "previous_questions": [1, 4, 20, 15]
    "quiz_category": "current category"
 }
```

- Returns: a single new question object

```json
{
  "question": {
    "id": 1,
    "question": "This is a question",
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 4
  }
}
```

---

`POST '/questions'`

- Sends a post request in order to add a new question <br/
>
Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What is your name?", "answer": "Aamad naseem abbasi","category" :"1", "difficulty":"2"}'`
- Request Body:

```json
{
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```


- Returns:
```json
{
    "created": 26,
    "success": true
}
```

---

`POST '/questions'`

- Sends a post request in order to search for a specific question by search term <br/>
Sample: `curl http://127.0.0.1:5000/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"ammad"}'`
- Request Body:

```json
{
  "searchTerm": "this is the term the user is looking for"
}
```

- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "Entertainment"
}
```

# Deployment N/A
# Authors: Aamad Naseem

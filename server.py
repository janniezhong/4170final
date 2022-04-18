from urllib import response
from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
from collections import defaultdict
app = Flask(__name__)

lessons = {
    "1": {
        "lesson_id": "1",
        "title": "Getting Started",
        "text": "let's get started! \r\n\r\n grep is a command in the shell often used for researching. It's insanely useful - if you know how to use it well. \r\n\r\nLet's start with basic grep. At its simplest, grep can be used to search for words in files. This directory has a file with filename HappyBirthday, containing al the lyrics to the Happy Birthday song. To search the song for all lines with the word \"birthday\", try typing \"grep \"birthday\" HappyBirthday\". Don't forget your doable quotes!",
        "answer": "grep \"birthday\" HappyBirthday",
        "next_lesson_id": "2",
    },
    "2": {
        "lesson_id": "2",
        "title": "searching for dear",
        "text": "Happy birthday to you\r\n Happy birthday to you\r\n Happy birthday, dear [name]\r\n Happy brithday to you. \r\n\r\nSuccess! Now try searching forall lines with the word\"dear\".",
        "answer": "grep \"dear\" HappyBirthday",
        "next_lesson_id": "3",
    },
    "3": {
        "lesson_id": "3",
        "title": "searching with whitespace",
        "text": "Happy birthday, dear [name]\r\n\r\nSince the thrid line is the only one that contains \"dear\", the terminal now only returns that line. grep isn't limited to just words and letters - it can serach for any string. Try searching for all lines with the string \"to you\"",
        "answer": "grep \"to you\" HappyBirthday",
        "next_lesson_id": "4",
    },
    "4": {
        "lesson_id": "4",
        "title": "searching for multiple words",
        "text": "Happy birthday to you\r\n Happy birthday to you\r\n Happy brithday to you. \r\n\r\n Solid! Now what happens if we want to search for different strings at once (say \"you\" and \"dear\")? We can't just type \"you dear\", since as we saw in the last example that's what it'll search for directly.\nInstead, we use the pipe operator, \"|\", to indicate \"or\". Try typing \"grep \"you | dear\" HappyBirthday\".",
        "answer": "grep \"you | dear\" HappyBirthday",
        "next_lesson_id": "5",
    }
}

quiz_dict = {
    '1': {
        'quiz_id': '1',
        'title': 'Searching Through Recipes',
        'instruction': 'Various other readers are looking at a recipe book, and would like your assistance in searching through them as well. Use your new commands to help these people find what they need! If you need a hint, type and enter h.',
        'question': 'Person 1: My favorite condiments are ketchup and mustard. I’d like to find the names of recipes containing these ingredients in this recipe book.',
        'answer': '',
        'img': '/static/images/image1.png'
    },
    '2': {
        'quiz_id': '2',
        'title': 'Searching Through Recipes',
        'instruction': 'Various other readers are looking at some other books, and would like your assistance in searching through it as well. Use your new commands to help these people find what they need! If you need a hint, type and enter h.',
        'question': 'Person 2: I love salty food, especially things made with soy sauce. I’d like to find the names of recipes containing the words “salt” or “soy sauce” from this recipe book.',
        'answer': '',
        'img': '/static/images/image2.png'
    },
    '3': {
        'quiz_id': '3',
        'title': 'Searching Through Recipes',
        'instruction': 'Various other readers are looking at some other books, and would like your assistance in searching through it as well. Use your new commands to help these people find what they need! If you need a hint, type and enter h.',
        'question': 'Person 3: I’m interested in Recipe3 in this book. Unfortunately, I don’t have a Dutch oven: can you search Recipe3 for the phrase “dutch oven” (case insensitive), so I know whether it’s essential or not?',
        'answer': '',
        'img': '/static/images/image3.png'
    },
    '4': {
        'quiz_id': '4',
        'title': 'Searching Through Recipes',
        'instruction': 'Various other readers are looking at some other books, and would like your assistance in searching through it as well. Use your new commands to help these people find what they need! If you need a hint, type and enter h.',
        'question': 'Person 4: I love galettes, both savory and sweet. I’d like to find the names of all recipes that are making galettes in this book.',
        'answer': '',
        'img': '/static/images/image4.png'
    }
}

lesson_responses = {}

lesson_reponseId = 1

quiz_response = defaultdict(list)
quiz_score = {quiz_id : 0 for quiz_id in quiz_dict}

# ROUTES

@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/learn')
def learn():
    return render_template('learn.html')

@app.route('/quiz/<quiz_id>')
def quiz(quiz_id=None):
    return render_template('quiz.html', quiz_info=quiz_dict[quiz_id])

@app.route('/quiz/result')
def result():
    return render_template('result.html', score=sum(quiz_score.values()))

# ajax
@app.route('/next_lesson', methods=['GET', 'POST'])
def next_lesson():
    global lessons

    json_data=request.get_json()

    lesson_id = json_data["id"]
    lesson_response = json_data["response"]
    logResponse(lesson_id, lesson_response)
    print(lesson_id, lesson_response)

    current_lesson = lessons[lesson_id]
    return jsonify(current_lesson)


@app.route('/save_response', methods=['POST'])
def save_response():
    json_data=request.get_json()

    id = json_data["id"]
    response = json_data["response"]
    quiz_response[id].append(response)
    quiz_score[id] = 1 if quiz[id]['answer'] == response else 0

    return jsonify(quiz_response)

# methods

def logResponse(lesson_id, lesson_response):

    global lesson_reponseId
    global lesson_responses

    response_entry = {"lesson_id": lesson_id,
                      "response": lesson_response}
    id = str(lesson_reponseId)
    lesson_responses.update({id:response_entry})
    print (lesson_responses)



if __name__ == '__main__':
   app.run(debug = True)





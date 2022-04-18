from urllib import response
from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
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
    },
    "5": {
        "lesson_id": "5",
        "title": "searching for words and punctuation",
        "text": "\r\nHappy birthday to you\r\n Happy birthday to you\r\n Happy birthday, dear [name]\r\n Happy brithday to you.\r\n\r\n Since every line contains either \"you\" or \"dear\", the terminal return every line. Perfect!\r\n How would you search for lines that contain \"to\" and \",\"?", 
        "answer": "grep \"to | ,\" HappyBirthday",
        "next_lesson_id": "6",
    },
    "6": {
        "lesson_id": "6",
        "title": "searching through new song BlackSheep",
        "text": "\r\nHappy birthday to you\r\n Happy birthday to you\r\n Happy birthday, dear [name]\r\n Happy brithday to you.\r\n\r\n Again, since every line contains either \"to\" or \",\", the terminal returned every line. Let's move on to something a little more difficult :)\r\n\r\n Let's imagine that we're now searching through a different file in the same folder titled \"BlackSheep\" that contains all the lyrics to the children's nursery rhyme \"Baa Baa Black Sheep\", but with random capitalization throughout.\r\nTry searching for the word \"wool\" in this file.",
        "answer": "grep \"wool\" BlackSheep",
        "next_lesson_id": "7",
    },
     "7": {
        "lesson_id": "7",
        "title": "teaching the -i flag part 1",
        "text": "\r\n\r\n That's weird It seems like no lines contain the word \"wool\". Maybe that's becasue of the random capitalization (grep \"wool\" BlackSheep only searches for lines with the word \"wool\" where all letters are lowercase).\r\nInstead try typing \"grep -i \"wool\" BlackSheep.",
        "answer": "grep -i \"wool\" BlackSheep.",
        "next_lesson_id": "8",
    },
    "8": {
        "lesson_id": "7",
        "title": "teaching the -i flag part 2",
        "text": "\r\n\r\n That's weird It seems like no lines contain the word \"wool\". Maybe that's becasue of the random capitalization (grep \"wool\" BlackSheep only searches for lines with the word \"wool\" where all letters are lowercase).\r\nInstead try typing \"grep -i \"wool\" BlackSheep.",
        "answer": "grep -i \"wool\" BlackSheep.",
        "next_lesson_id": "8",
    }
}

lesson_responses = {}

lesson_reponseId = 1
# ROUTES

@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/learn')
def learn():
    return render_template('learn.html')

@app.route('/quiz/<quiz_id>')
def quiz():
    return render_template('quiz.html')

@app.route('/quiz/result/<quiz_score>')
def quizscore():
    return render_template('quizresult.html')

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





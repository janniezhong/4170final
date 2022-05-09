# from urllib import Response
from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
from collections import defaultdict

from checker import check_quiz_answers

app = Flask(__name__)

lessons = {
    "1": {
        "chapter": "grep basics",
        "chapter_id": "1",
        "lesson_id": "1",
        "topic": "How to search for words in files I",
        "prompt": "grep is a command in the shell often used for searching.\r\n\r\nAt its simplest, grep can be used to search for words in files.",
        "feedback": "Looks good! grep is the command, \"birthday\" is the string to search for, and HappyBirthday.txt is the file in which to look for it.",
        "instruction": "Try typing \"grep \"star\" TwinkleTwinkle.txt\" in the terminal.",
        "answer": "grep \"star\" TwinkleTwinkle.txt",
        "response": "Twinkle, twinkle, little star\r\nTwinkle, twinkle, little star\r\n",
        "previous_lesson_id": "1",
        "next_lesson_id": "2",
    },
    "2": {
        "chapter": "grep basics",
        "chapter_id": "1",
        "lesson_id": "2",
        "topic": "How to search for words in files II",
        "prompt": "Success! Now try searching for all lines with the word\r\n \"diamond\"",
        "feedback": "Since the fourth line is the only one that contains \"diamond\", the terminal now only returns that line.",
        "instruction": "",
        "answer": "grep \"diamond\" TwinkleTwinkle.txt",
        "response": "Like a diamond in the sky",
        "previous_lesson_id": "1",
        "next_lesson_id": "3",
    },
    "3": {
        "chapter": "grep basics",
        "chapter_id": "1",
        "lesson_id": "3",
        "topic": "How to search for multiple strings",
        "prompt": "If we want to search for different strings at once,\r\n(say \"star\" and \"diamond\") we use the pipe operator, \"|\", to indicate \"or\".",
        "feedback": "Every line contains either \"star\" or \"diamond\".",
        "instruction": "Try typing \"grep \"star | diamond\" TwinkleTwinkle.txt\".",
        "answer": "grep \"star | diamond\" TwinkleTwinkle.txt",
        "response": "Twinkle, twinkle, little star\r\nLike a diamond in the sky\r\nTwinkle, twinkle, little star\r\n",
        "previous_lesson_id": "2",
        "next_lesson_id": "4",
    },
    "4": {
        "chapter": "grep basics",
        "chapter_id": "1",
        "lesson_id": "4",
        "topic": "Search for multiple non-alphabetical strings",
        "prompt": "How would you search for lines that contain \"wonder\" or a comma(\",\")?",
        "feedback": "Again, every line contains either \"wonder\" or \",\".",
        "instruction": "",
        "answer": "grep \"wonder | ,\" TwinkleTwinkle.txt",
        "response": "Twinkle, twinkle, little star\r\nHow I wonder what you are\r\nTwinkle, twinkle, little star\r\n",
        "previous_lesson_id": "3",
        "next_lesson_id": "5",
    },
    "5": {
        "chapter": "The -i flag",
        "chapter_id": "2",
        "lesson_id": "5",
        "topic": "Search through a new song",
        "prompt": "The file \"BlackSheep.txt\" contains the lyrics to the rhyme \"Baa Baa Black Sheep\"\r\n\r\nSearch for lines of the song that contain the word \"wool\"",
        "feedback": "Cool!",
        "instruction": "",
        "answer": "grep \"wool\" BlackSheep.txt",
        "response": "Have you any wool?",
        "previous_lesson_id": "4",
        "next_lesson_id": "6",
    },
    "6": {
        "chapter": "The -i flag",
        "chapter_id": "2",
        "lesson_id": "6",
        "topic": "Search for the word \"one\".",
        "prompt": "Now search the file BlackSheep.txt for the lines of the song that contain the word \"one\".",
        "feedback": "Weird! grep only found one instance of the word \"one\", but we know that the song has:\r\n\"one for the master\"\r\n\"one for the dame\"\r\n\"one for the little boy that lives down the lane\".",
        "instruction": "",
        "answer": "grep \"one\" BlackSheep.txt",
        "response": "And one for the little boy that lives down the lane",
        "previous_lesson_id": "5",
        "next_lesson_id": "7",
    },
    "7": {
        "chapter": "The -i flag",
        "chapter_id": "2",
        "lesson_id": "7",
        "topic": "Case-insensitive search 1",
        "prompt": "Maybe the song has both the lines:\r\n\"one for the master\"\r\n\"one for the dame\"\r\nBut the word \"one\" in those lines is capitalised.",
        "feedback": "The \"-i\" flag we added to the command indicates that the search string should be case insensitive - it\'ll search for \"one\", \"One\", even \"oNe\".",
        "instruction": "Try typing \"grep -i \"one\" BlackSheep.txt\".",
        "answer": "grep -i \"one\" BlackSheep.txt",
        "response": "One for the master,\r\nOne for the dame,\r\none for the little boy that lives down the lane.",
        "previous_lesson_id": "6",
        "next_lesson_id": "8",
    },
    "8": {
        "chapter": "The -i flag",
        "chapter_id": "2",
        "lesson_id": "8",
        "topic": "Case-insensitive search 2",
        "prompt": "Try to search for the string \"oNe\" in the BlackSheep.txt file, case insensitive.",
        "feedback": "It returns the same thing; as it should!",
        "instruction": "",
        "answer": "grep -i \"oNe\" BlackSheep.txt",
        "response": "One for the master,\r\nOne for the dame,\r\none for the little boy that lives down the lane.",
        "previous_lesson_id": "7",
        "next_lesson_id": "9",
    },
    "9": {
        "chapter": "Using * with grep",
        "chapter_id": "3",
        "lesson_id": "9",
        "topic": "Searching through the current directory",
        "prompt": "Search for all instances of the word \"little\" in the current directory.",
        "feedback": "\"*\" indicates that you\'d like to search through the whole directory that you\'re currently in.",
        "instruction": "Type \"grep -i \"little\" *\"",
        "answer": "grep -i \"little\" *",
        "response": "BlackSheep.txt:And one for the little boy\r\nTwinkle.txt:Twinkle, twinkle, little star,\r\nTwinkle.txt:Twinkle, twinkle, little star,\r\nTeapot.txt:I\'m a little teapot",
        "previous_lesson_id": "8",
        "next_lesson_id": "10",
    },
    "10": {
        "chapter": "The -l flag",
        "chapter_id": "4",
        "lesson_id": "10",
        "topic": "Searching for just the file name 1",
        "prompt": "Try searching this directory for the word \"shark\" (case insensitive).",
        "feedback": "Woah that\'s a lot. If only there were a way for us to only search for the file name...",
        "instruction": "",
        "answer": "grep -i \"shark\" *",
        "response": "BabyShark.txt:Baby shark, doo, doo, doo, doo, doo, doo.\r\nBabyShark.txt:Baby shark, doo, doo, doo, doo, doo, doo.\r\nBabyShark.txt:Baby shark, doo, doo, doo, doo, doo, doo.\r\nBabyShark.txt:Baby shark!\r\nBabyShark.txt:Mommy shark, doo, doo, doo, doo, doo, doo.\r\nBabyShark.txt:Mommy shark, doo, doo, doo, doo, doo, doo.\r\nBabyShark.txt:Mommy shark, doo, doo, doo, doo, doo, doo.\r\nBabyShark.txt:Mommy shark!\r\nBabyShark.txt:Daddy shark, doo, doo, doo, doo, doo, doo.\r\nBabyShark.txt:Daddy shark, doo, doo, doo, doo, doo, doo.\r\nBabyShark.txt:Daddy shark, doo, doo, doo, doo, doo, doo.\r\nBabyShark.txt:Daddy shark!\r\nBabyShark.txt:Grandma shark, doo, doo, doo, doo, doo, doo.\r\nBabyShark.txt:Grandma shark, doo, doo, doo, doo, doo, doo.\r\nBabyShark.txt:Grandma shark, doo, doo, doo, doo, doo, doo.\r\nBabyShark.txt:Grandma shark!\r\nBabyShark.txt:Grandpa shark, doo, doo, doo, doo, doo, doo.\r\nBabyShark.txt:Grandpa shark, doo, doo, doo, doo, doo, doo.\r\nBabyShark.txt:Grandpa shark, doo, doo, doo, doo, doo, doo.\r\nBabyShark.txt:Grandpa shark!\r\n",
        "previous_lesson_id": "9",
        "next_lesson_id": "11",
    },
    "11": {
        "chapter": "The -l flag",
        "chapter_id": "4",
        "lesson_id": "11",
        "topic": "Searching for just the file name 2",
        "prompt": "Try typing \"grep -l \"shark\" *\" to remove duplicates of files that contain the search term.",
        "feedback": "The \"-l\" flag shows the file name in which the string was found, and not the line itself - removing duplicates.",
        "instruction": "Type \"grep -l \"shark\" *\".",
        "answer": "grep -l \"shark\" *",
        "response": "BabyShark.txt",
        "previous_lesson_id": "10",
        "next_lesson_id": "12",
    },
    "12": {
        "chapter": "The -r flag",
        "chapter_id": "5",
        "lesson_id": "12",
        "topic": "Searching folders within directories 1",
        "prompt": "The current directory contains a folder titled \"favorite\" which contains the file \"HumptyDumpty\".",
        "feedback": "grep\'s search function doesn\'t extend beyond the present working directory",
        "instruction": "Type \"grep \"horses\" *\".",
        "answer": "grep \"horses\" *",
        "response": "",
        "previous_lesson_id": "11",
        "next_lesson_id": "13",
    },
    "13": {
        "chapter": "The -r flag",
        "chapter_id": "5",
        "lesson_id": "13",
        "topic": "Searching folders within directories 2",
        "prompt": "Extend the range of the search to folders within the current directory.",
        "feedback": "The -r flag allows grep to search through all files in the current directory, and all files within folders in the current directory.",
        "instruction": "Type \"grep -r \"horses\" *\".",
        "answer": "grep -r \"horses\" *",
        "response": "favorite\HumptyDumpty.txt: All the king\'s horses",
        "previous_lesson_id": "12",
        "next_lesson_id": "final",
    },
    "final": {
        "chapter": "Combining flags",
        "chapter_id": "6",
        "lesson_id": "final",
        "topic": "How to combine flags",
        "prompt": "To search case insensitively, for only the file name, across all folders within the current directory, you can either type \"-l -i -r\" or \"-lir\".",
        "feedback": "Looks good! You/'re a grep rockstar - time to put all that knowledge to the test!",
        "instruction": "Type \"grep -lir \"and\" *\".",
        "answer": "grep -lir \"and\" *",
        "response": "Teapot.txt\r\nfavorite\HumptyDumpty.txt",
        "previous_lesson_id": "13",
        "next_lesson_id": "",
    },

}

quiz_dict = {
    '1': {
        'quiz_id': '1',
        'title': 'Quiz 1',
        'instruction': 'If you need a hint, type and enter h.',
        'question': 'You are trying to find all recipes that use an onion. How would you find them?',
        'valid_flags': '',
        'valid_pattern': ['onion'],
        'valid_file': 'recipe_book/*',
        'img': '/static/images/image1.png',
        'answer': 'grep -R onion recipe_book'
    },
    '2': {
        'quiz_id': '2',
        'title': 'Quiz 2',
        'instruction': 'If you need a hint, type and enter h.',
        'question': 'Now, you want all recipes that use both salt and mustard. How would you find them?',
        'valid_flags': 'E',
        'valid_pattern': ['mustard', 'salt'],
        'valid_file': '*',
        'img': '/static/images/image2.png',
        'answer': 'grep -RE \"mustard|salt\" recipe_book'
    },
    '3': {
        'quiz_id': '3',
        'title': 'Quiz 3',
        'instruction': 'If you need a hint, type and enter h.',
        'question': 'You are trying to check if recipe4 uses a carrot, but the letter cases are messed up. How would you check if recipe4 uses a carrot?',
        'valid_flags': 'i',
        'valid_pattern': ['carrot'],
        'valid_file': 'recipe4',
        'img': '/static/images/image3.png',
        'answer': 'grep -i carrot recipe_book/recipe4'
    },
    '4': {
        'quiz_id': '4',
        'title': 'Searching Through Recipes',
        'instruction': 'If you need a hint, type and enter h.',
        'question': 'The recipe book now has two sections: savory recipes and sweet recipes. However, you don\'t care taste and want to find all recipes that use garlic. How would you find them?',
        'valid_flags': 'r',
        'valid_pattern': ['garlic'],
        'valid_file': '/recipe_book',
        'img': '/static/images/image4.png',
        'answer': 'grep -R garlic recipe_book'
    }
}

lesson_responses = {}

lesson_reponseId = 1

quiz_response = defaultdict(list)

# key needs to be int to be jsonified
quiz_score = {int(quiz_id): 0 for quiz_id in quiz_dict}


def navbar_info():
    global lessons
    global quiz_dict
    navbar_info = {}
    navbar_info["num_lessons"] = len(lessons.keys())
    navbar_info["num_quizzes"] = len(quiz_dict.keys())
    return navbar_info


# ROUTES

@app.route('/')
def home():
    return render_template('index.html', navbar_info=navbar_info())


@app.route('/learn/<lesson_id>')
def learn(lesson_id=None):
    return render_template('learn.html', lesson_info=lessons[lesson_id], navbar_info=navbar_info())


@app.route('/quiz/<quiz_id>')
def quiz(quiz_id=None):
    return render_template('quiz.html', quiz_info=quiz_dict[quiz_id], navbar_info=navbar_info())


@app.route('/result')
def result():
    return render_template('result.html', score=sum(quiz_score.values()), navbar_info=navbar_info())

# ajax


@app.route('/check_answer', methods=['GET', 'POST'])
def check_answer():
    global lessons

    json_data = request.get_json()

    lesson_id = json_data["id"]
    lesson_response = json_data["response"]
    log_response(lesson_id, lesson_response)
    print(lesson_id, lesson_response)
    lesson_return = {"correct": "true",
                     "error": ""}
    if lesson_response == lessons[lesson_id]["answer"]:
        return jsonify(lesson_return)
    else:
        lesson_return["correct"] = "false"
        lesson_return["error"] = "MISC. error"
        return jsonify(lesson_return)


@app.route('/save_response', methods=['POST'])
def save_response():
    json_data = request.get_json()

    id = json_data["id"]
    response = json_data["response"]
    quiz_response[id].append(response)

    res = parse_request(id, response)

    quiz_score[id] = 1 if res else 0

    return jsonify(quiz_score[id])

# methods


def parse_request(qid, req):
    ret =  check_quiz_answers(quiz_dict[str(qid)]["answer"], req, qid)
    return ret[0]



def log_response(lesson_id, lesson_response):

    global lesson_reponseId
    global lesson_responses

    response_entry = {"lesson_id": lesson_id,
                      "response": lesson_response}
    id = str(lesson_reponseId)
    lesson_reponseId += 1
    lesson_responses.update({id: response_entry})
    print(lesson_responses)


if __name__ == '__main__':
    app.run(debug=True)

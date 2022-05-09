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
        "topic": "words in files",
        "prompt": "<span class = \"command\">grep</span> is a command in the shell often used for searching.\r\n\r\nAt its simplest, <span class = \"command\">grep</span> can be used to search for words in files.",
        "feedback": "Looks good! <span class = \"command\">grep</span> is the command, and \"<span class = \"search-string\">star</span>\" is the string to search for, and <span class = \"location\">TwinkleTwinkle.txt</span> is the file in which to look for it.",
        "instruction": "Try typing \"<span class=\"command\">grep</span> \"<span class = \"search-string\">star</span>\" <span class = \"location\">TwinkleTwinkle.txt</span>\" in the terminal.",
        "answer": "grep \"star\" TwinkleTwinkle.txt",
        "response": "Twinkle, twinkle, little star\r\nTwinkle, twinkle, little star\r\n",
        "previous_lesson_id": "1",
        "next_lesson_id": "2",
    },
    "2": {
        "chapter": "grep basics",
        "chapter_id": "1",
        "lesson_id": "2",
        "topic": "words in files",
        "prompt": "Success! Now try searching the same file (<span class = \"location\">TwinkleTwinkle.txt</span>) for all lines with the word\r\n \"<span class=\"search-string\">diamond</span>\".",
        "feedback": "Since the fourth line is the only one that contains \"<span class=\"search-string\">diamond</span>\", the terminal now only returns that line.",
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
        "topic": "multiple strings",
        "prompt": "If we want to search for different strings at once,\r\n(say \"<span class = \"search-string\">star</span>\" and \"<span class=\"search-string\">diamond</span>\") we use the pipe operator, \"|\", to indicate <b>or<b>.",
        "feedback": "Every line contains either \"<span class = \"search-string\">star</span>\" or \"<span class=\"search-string\">diamond</span>\".",
        "instruction": "Try typing \"<span class = \"command\">grep</span> \"<span class = \"search-string\">star</span>|<span class=\"search-string\">diamond</span>\" <span class = \"location\">TwinkleTwinkle.txt</span>\".",
        "answer": "grep \"star|diamond\" TwinkleTwinkle.txt",
        "response": "Twinkle, twinkle, little star\r\nLike a diamond in the sky\r\nTwinkle, twinkle, little star\r\n",
        "previous_lesson_id": "2",
        "next_lesson_id": "4",
    },
    "4": {
        "chapter": "grep basics",
        "chapter_id": "1",
        "lesson_id": "4",
        "topic": "multiple strings",
        "prompt": "How would you search the <span class = \"location\">TwinkleTwinkle.txt</span> file for lines that contain \"<span class = \"search-string\">wonder</span>\" or a comma(\"<span class = \"search-string\">,</span>\")?",
        "feedback": "Again, every line contains either \"<span class = \"search-string\">wonder</span>\" or \"<span class = \"search-string\">,</span>\".",
        "instruction": "",
        "answer": "grep \"wonder|,\" TwinkleTwinkle.txt",
        "response": "Twinkle, twinkle, little star\r\nHow I wonder what you are\r\nTwinkle, twinkle, little star\r\n",
        "previous_lesson_id": "3",
        "next_lesson_id": "5",
    },
    "5": {
        "chapter": "The -i flag",
        "chapter_id": "2",
        "lesson_id": "5",
        "topic": "a new song file",
        "prompt": "The file \"<span class = \"location\">BlackSheep.txt</span>\" contains the lyrics to the rhyme \"Baa Baa Black Sheep\".\r\n\r\nSearch for lines of the song that contain the word \"<span class = \"search-string\">wool</span>\".",
        "feedback": "Cool - you should have no problem with this by now!",
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
        "topic": "an incomplete result?",
        "prompt": "Now search the file <span class = \"location\">BlackSheep.txt</span> for the lines of the song that contain the word \"<span class = \"search-string\">one</span>\".",
        "feedback": "Weird! <span class = \"command\">grep</span> only found one instance of the word \"<span class = \"search-string\">one</span>\", but we know that the song has:\r\n\"one for the master\",\r\n\"one for the dame\",\r\n\"one for the little boy that lives down the lane\".\r\nMaybe we're missing something?",
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
        "topic": "searching case-insensitively",
        "prompt": "Maybe the song has both the lines:\r\n\"<span class = \"search-string\">one</span> for the master\"\r\n\"<span class = \"search-string\">one</span> for the dame\"\r\nBut the word \"<span class = \"search-string\">one</span>\" in those lines is capitalised.",
        "feedback": "The \"<span class = \"flags\">-i</span>\" flag we added to the command indicates that the search string should be case insensitive - it\'ll search for \"<span class = \"search-string\">one</span>\", \"<span class = \"search-string\">One</span>\", even \"<span class = \"search-string\">oNE</span>\".",
        "instruction": "Try typing \"<span class = \"command\">grep</span> <span class = \"flags\">-i</span> \"<span class = \"search-string\">one</span>\" <span class = \"location\">BlackSheep.txt</span>\".",
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
        "prompt": "Try to search for the string \"<span class = \"search-string\">oNe</span>\" in the <span class = \"location\">BlackSheep.txt</span> file, case insensitive.",
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
        "prompt": "Search for all instances of the word \"<span class = \"search-string\">little</span>\" in the <span class = \"location\">Current Directory</span>.",
        "feedback": "\"<span class = \"location\">*</span>\" indicates that you\'d like to search through the whole directory that you\'re currently in.",
        "instruction": "Type \"<span class = \"command\">grep</span> <span class = \"flags\">-i</span> \"<span class = \"search-string\">little</span>\" <span class = \"location\">*</span>\"",
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
        "prompt": "Try searching <span class = \"location\">this directory</span> for the word \"<span class = \"search-string\">shark</span>\" (case insensitive).",
        "feedback": "Woah that\'s a lot of lines. If only there were a way for us to search and have the terminal ONLY respond with the file name of interest (without all the noise...)",
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
        "prompt": "The inclusion of the <span class = \"flags\">-l</span> flag in ther terminal command: \"<span class = \"command\">grep</span> <span class = \"flags\">-l</span> \"<span class = \"search-string\">shark</span>\" <span class = \"location\">*</span>\" will remove duplicates of files that contain the search term multiple times.",
        "feedback": "The \"<span class = \"flags\">-l</span>\" flag shows the file name in which the string was found, and not each line itself - removing duplicates.",
        "instruction": "Type \"<span class = \"command\">grep</span> <span class = \"flags\">-l</span> \"<span class = \"search-string\">shark</span>\" <span class = \"location\">*</span>\".",
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
        "prompt": "The current directory contains a folder titled \"<span class = \"location\">favorite</span>\" which contains the file \"<span class = \"location\">HumptyDumpty.txt</span>\".",
        "feedback": "Surprised that there's no results? That's because <span class = \"command\">grep</span>\'s search function doesn\'t extend beyond the present working directory - meaning by default it won't look within folders.",
        "instruction": "Type \"<span class = \"command\">grep</span> \"<span class = \"search-string\">horses</span>\" <span class = \"location\">*</span>\".",
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
        "prompt": "Extend the range of the search to encompass folders within the current directory.",
        "feedback": "The <span class = \"flags\">-r</span> flag allows <span class = \"command\">grep</span> to search through all files in the current directory, and all files within folders in the current directory.",
        "instruction": "Type \"<span class = \"command\">grep</span> <span class = \"flags\">-r</span> \"<span class = \"search-string\">horses</span>\" <span class = \"location\">*</span>\".",
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
        "prompt": "To search case insensitively, for only the file name, across all folders within the current directory, you can either type <p>\"<span class = \"flags\">-l</span> <span class = \"flags\">-i</span> <span class = \"flags\">-r</span>\" or \"<span class = \"flags\">-lir</span>\".</p><p>Let's generalize our search by looking for files that contain the word \"<span class = \"search-string\">and</span>\" (case insensitive)</p>",
        "feedback": "Looks good - now you know how to use multiple flags at once! You\'re a <span class = \"command\">grep</span> rockstar - time to put all that knowledge to the test!",
        "instruction": "Type \"<span class = \"command\">grep</span> <span class = \"flags\">-lir</span> \"<span class = \"search-string\">and</span>\" <span class = \"location\">*</span>\".",
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
        'question': 'You are at home directory (~/) that has recipe_book (directory). You have recipe_book that contains recipes (files), and you are trying to find recipes that use onion (case-sensitive) in recipe_book. How would you find them?',
        'answer': 'grep -r onion recipe_book'
    },
    '2': {
        'quiz_id': '2',
        'title': 'Quiz 2',
        'question': 'Now, you want recipes (files) that use both salt and mustard in recipe_book (directory). How would you find them? Note that you are still in home directory and salt and mustard are case-sensitive',
        'answer': 'grep -rE "mustard|salt" recipe_book'
    },
    '3': {
        'quiz_id': '3',
        'title': 'Quiz 3',
        'question': 'You are trying to check if recipe4 (a file in recipe_book directory) uses a carrot, but the letter cases are messed up How would you check if recipe4 uses a carrot? Note that the word you are trying to search is carrot (case-sensitive), but recipe4 may have carrot as cArrOT, CaRRot, etc...',
        'answer': 'grep -i carrot recipe_book/recipe4'
    },
    '4': {
        'quiz_id': '4',
        'title': 'Quiz 4',
        'question': 'The recipe book (directory) now has two sections: savory recipes (directory in recipe_book) and sweet recipes (directory in recipe_book). However, you don\'t care taste and want to find all recipes that use garlic. How would you find them? Note that you are still in home directory and trying to find all recipes in recipe_book',
        'answer': 'grep -r garlic recipe_book'
    },
    '5': {
        'quiz_id': '5',
        'title': 'Quiz 5',
        'question': 'You found out that the letter cases for garlic are also messed up. How would you find them? Note that the word you are trying to search is garlic (case-sensitive), but there may be recipes that have garlic as GARLIC, garLiC, gARliC, etc...',
        'answer': 'grep -iR garlic recipe_book'
    },
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
    
    parsed_res = parse_request(lesson_id, lesson_response, False)

    if parsed_res == "Correct!":
        return jsonify(lesson_return)
    else:
        lesson_return["correct"] = "false"
        lesson_return["error"] = parsed_res
        return jsonify(lesson_return)


@app.route('/save_response', methods=['POST'])
def save_response():
    json_data = request.get_json()

    uid = json_data["id"]
    response = json_data["response"]
    quiz_response[uid].append(response)

    res = parse_request(uid, response)

    quiz_score[uid] = 1 if res == 'Correct!' else 0

    return jsonify(res)

# methods


def parse_request(uid, req, quiz=True):
    req = list(req.split())
    ans = quiz_dict[str(uid)]['answer'].split() if quiz else lessons[uid]["answer"].split()
    flags, arr_without_flag = find_all_flag(req)

    if ans[1][0] == '-':
        if not flags:
            return 'Please use a flag(s) for this question'
        
        if flags != sorted(ans[1][1:]):
            return 'Please use a correct flag(s) for grep'
    else:
        if flags:
            return 'It seems you are trying to use unnecessary flag(s)'

    if arr_without_flag[0] != 'grep':
        return 'Please use grep as your first command of your answer'

    if len(arr_without_flag) != 3:
        return 'It seems you omitted or put exptra either pattern or file/directory'
    
    user_pattern = sorted(arr_without_flag[1].lstrip("\"").rstrip("\"").split("|"))

    pattern_idx = 2 if ans[1][0] == '-' else 1

    if '|' in arr_without_flag[pattern_idx] and arr_without_flag[pattern_idx][0] != '\"' and arr_without_flag[pattern_idx][-1] != '\"':
        return 'Please use a correct format for pattern' 

    ans_pattern = sorted(ans[pattern_idx].lstrip("\"").rstrip("\"").split("|"))

    if user_pattern != ans_pattern:
        return 'Please use a correct pattern'
    
    file_idx = 3 if ans[1][0] == '-' else 2
    if arr_without_flag[2] != ans[file_idx]:
        return 'Please search a correct file/directory'
    
    return 'Correct!'

def find_all_flag(arr):
    arr_no_flag = []
    flags = []
    for i, v in enumerate(arr):
        if v[0] == '-':
            flags += list(v[1:])
        else:
            arr_no_flag.append(v)
    return sorted(flags), arr_no_flag

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

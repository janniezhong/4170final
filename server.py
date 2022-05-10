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
        "prompt": "If we want to search for different strings at once,\r\n(say \"<span class = \"search-string\">star</span>\" and \"<span class=\"search-string\">diamond</span>\") we use the pipe operator, \"|\", along with the <span class = \"flags\">-E</span> flag to indicate <b>or</b>. Watch your capitalization — <span class = \"command\">grep</span> cares about capitalization in its flags.",
        "feedback": "Every line contains either \"<span class = \"search-string\">star</span>\" or \"<span class=\"search-string\">diamond</span>\".",
        "instruction": "Try typing \"<span class = \"command\">grep</span> <span class = \"flags\">-E</span> \"<span class = \"search-string\">star</span>|<span class=\"search-string\">diamond</span>\" <span class = \"location\">TwinkleTwinkle.txt</span>\". The backslash acts as a escape character.",
        "answer": "grep -E \"star|diamond\" TwinkleTwinkle.txt",
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
        "answer": "grep -E \"wonder|,\" TwinkleTwinkle.txt",
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
        "prompt": "The song has both the lines:\r\n\"<span class = \"search-string\">One</span> for the master\"\r\n\"<span class = \"search-string\">One</span> for the dame\". \r\n However, the word \"<span class = \"search-string\">one</span>\" in those lines is capitalised, so grep doesn't pick them up.",
        "feedback": "The \"<span class = \"flags\">-i</span>\" flag we added to the command indicates that the search string should be case insensitive - it\'ll search for \"<span class = \"search-string\">one</span>\", \"<span class = \"search-string\">One</span>\", even \"<span class = \"search-string\">oNE</span>\".",
        "instruction": "To handle capitalization, try typing \"<span class = \"command\">grep</span> <span class = \"flags\">-i</span> \"<span class = \"search-string\">one</span>\" <span class = \"location\">BlackSheep.txt</span>\".",
        "answer": "grep -i \"one\" BlackSheep.txt",
        "response": "One for the master,\r\nOne for the dame,\r\none for the little boy that lives down the lane.",
        "previous_lesson_id": "6",
        "next_lesson_id": "8",
    },
    "8": {
        "chapter": "The -i flag",
        "chapter_id": "2",
        "lesson_id": "8",
        "topic": "searching case-insensitively",
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
        "topic": "searching through the current directory",
        "prompt": "In order to search through all files in the current directory, we can use the asterisk. Let's try searching for all instances of the word \"<span class = \"search-string\">little</span>\" in the <span class = \"location\">current directory</span>.",
        "feedback": "\"<span class = \"location\">*</span>\" indicates that you\'d like to search through the whole directory that you\'re currently in, and returns lines as well as filenames.",
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
        "topic": "searching for the filename",
        "prompt": "How would you search this directory for <span class = \"location\">this directory</span> for the word \"<span class = \"search-string\">shark</span>\" (case insensitive)?",
        "feedback": "Woah, that\'s a lot of lines. If only there were a way for us to search and have the terminal ONLY respond with the filename of interest (without all the noise...)",
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
        "topic": "searching for just the filename",
        "prompt": "The <span class = \"flags\">-l</span> flag will ask <span class = \"command\">grep</span> for just the filename, and will remove duplicates of files that contain the search term multiple times.",
        "feedback": "The \"<span class = \"flags\">-l</span>\" flag shows the file name in which the string was found, and not each line itself.",
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
        "topic": "searching in files inside directories",
        "prompt": "The current directory contains a folder titled \"<span class = \"location\">favorite</span>\" which contains the file \"<span class = \"location\">HumptyDumpty.txt</span>\".",
        "feedback": "There are no results! That's because <span class = \"command\">grep</span>\'s search function doesn\'t extend beyond the present working directory - meaning that, by default, it won't look within folders. We can solve this with another flag.",
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
        "topic": "searching in files inside directories",
        "prompt": "Extend the range of the search to encompass folders within the current directory by using the <span class = \"flags\">-r</span> flag.",
        "feedback": "The <span class = \"flags\">-r</span> flag allows <span class = \"command\">grep</span> to search through all files in the current directory, as well as all files within folders in the current directory.",
        "instruction": "Type \"<span class = \"command\">grep</span> <span class = \"flags\">-r</span> \"<span class = \"search-string\">horses</span>\" <span class = \"location\">*</span>\".",
        "answer": "grep -r \"horses\" *",
        "response": "favorite\HumptyDumpty.txt: All the king\'s horses",
        "previous_lesson_id": "12",
        "next_lesson_id": "final",
    },
    "final": {
        "chapter": "combining flags",
        "chapter_id": "6",
        "lesson_id": "final",
        "topic": "How to combine flags",
        "prompt": "To search case insensitively, for only the file name, <b>and</b> across all folders within the current directory, you can either type \"<span class = \"flags\">-l</span> <span class = \"flags\">-i</span> <span class = \"flags\">-r</span>\", \"<span class = \"flags\">-lir</span>\", or \"<span class = \"flags\">-irl</span>\". <br> <br><p>Let's generalize our search by looking for <span class = \"flags\">filenames</span> that contain the word \"<span class = \"search-string\">and</span>\" (case insensitive), in <span class = \"location\">this directory</span> and <span class = \"location\">all sub-directories</span>.</p>",
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
        'question': 'You are in a directory that has a directory <span class = \"location\">recipe_book</span>. The <span class = \"location\">recipe_book</span> that contains recipes (files), and you are trying to find recipes that use \"<span class = \"search-string\">onion</span>\" <span class = \"flags\">(case-sensitive)</span> in <span class = \"location\">recipe_book</span>. How would you find them?',
        'answer': 'grep -r "onion" recipe_book'
    },
    '2': {
        'quiz_id': '2',
        'title': 'Quiz 2',
        'question': 'Now,"re you want the <span class = \"flags\">names</span> of recipes that use both \"<span class = \"search-string\">salt</span>\" and \"<span class = \"search-string\">mustard</span>\" in <span class = \"location\">recipe_book</span>. How would you find them? salt and mustard are <span class = \"flags\">case-sensitive</span>.',
        'answer': 'grep -rlE "mustard|salt" recipe_book'
    },
    '3': {
        'quiz_id': '3',
        'title': 'Quiz 3',
        'question': 'You now move into the recipe_book directory. You are trying to check if <span class = \"location\">recipe4.txt</span> uses a carrot, but the letter cases are messed up (\"Carrot\", \"caRrot\"). How would you check if <span class = \"location\">recipe4.txt</span> uses a \"<span class = \"search-string\">carrot</span>\", <span class = \"flags\">case-insensitive</span>?',
        'answer': 'grep -i "carrot" recipe4.txt'
    },
    '4': {
        'quiz_id': '4',
        'title': 'Quiz 4',
        'question': 'You are now in the <span class = \"location\">new_recipe_book</span> directory that has two sub-directories: savory recipes and sweet recipes. However, you just want to find all recipes (in both subdirectories) that use \"<span class = \"search-string\">garlic</span>\", <span class = \"flags\">case-sensitive</span>. How would you find them?',
        'answer': 'grep -r "garlic" *'
    },
    '5': {
        'quiz_id': '5',
        'title': 'Quiz 5',
        'question': 'You find that the letter cases for garlic are also messed up. How would you find them? Note that the word you are trying to search is garlic (case-sensitive), but there may be recipes that have garlic as GARLIC, garLiC, gARliC, etc...',
        'answer': 'grep -ir "garlic" *'
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
        return 'Too many arguments!'
    
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

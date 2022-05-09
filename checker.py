import subprocess
import shlex

# use subprocess to do the checking
# returns (boolean, string) that respectively indicate
# whether the user input was correct and help string in
# case it was not
def check_quiz_answers(answer, user_input, qid):
    answer = answer.strip()
    user_input = user_input.strip()

    cwd = get_cwd(qid)

    sec = security_check(user_input)

    if not sec[0]:
        return sec

    try:
        ans_out = subprocess.run(
            answer, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, shell=True, timeout=3, cwd=cwd)
    except subprocess.TimeoutExpired:
        return (False, "Reference answer execution timed out.")

    try:
        user_out = subprocess.run(
            user_input, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, shell=True, timeout=3, cwd=cwd)
    except subprocess.TimeoutExpired:
        return (False, "User answer execution timed out.")


    if user_out.returncode == 0:
        ret = compare_outputs(ans_out.stdout, user_out.stdout)
        if ret:
            return (ret, "Correct!")
        else:
            return (False, "Unexpected lines matched.")
    elif user_out.returncode == 1:
        return (False, "No lines matched.")

    return (False, "\r\n ".join(user_out.stderr.split('\n')))


def get_cwd(qid):
    quiz123 = [1, 2, 3]
    quiz4 = [4]

    if qid in quiz123:
        return "quiz/quiz123/"

    if qid in quiz4:
        return "quiz/quiz4/"

    return "quiz/quiz123/"


def security_check(user_input):
    filters = ['&&', '|', '||', 'sudo']
    invalid_paths = ['.', '..']

    tokens = shlex.split(user_input)

    if tokens[0] != 'grep':
        return False, "Please make sure grep is the first argument."

    if set(filters).intersection(set(tokens)):
        return False, "Please don't use dangerous keywords"

    if set(invalid_paths).intersection(set(tokens)):
        return False, ". and .. are not allowed."

    for p in tokens:
        if p[0] != '-':
            if '.' in p or '..' in p:
                return False, ". and .. are not allowed"

    return True, ""

def compare_outputs(ans_out, user_out):
    ans = ans_out.split('\n')
    user = user_out.split('\n')

    return sorted(ans) == sorted(user)

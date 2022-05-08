import subprocess


# use subprocess to do the checking
# returns (boolean, string) that respectively indicate
# whether the user input was correct and help string in
# case it was not
def check_quiz_answers(answer, user_input, qid):
    answer = answer.strip()
    user_input = user_input.strip()

    cwd = get_cwd(qid)

    if not security_check(user_input):
        return (False, "Please make sure grep is the first argument.")

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

    return (False, "Please try again")


def get_cwd(qid):
    quiz123 = [1, 2, 3]
    quiz4 = [4]

    if qid in quiz123:
        return "quiz/quiz123/"

    if qid in quiz4:
        return "quiz/quiz4"

    return "quiz/quiz123/"


def security_check(user_input):
    # for now just check the user is running grep
    tokens = user_input.split(" ")

    if tokens[0] != "grep":
        return False

    return True

def compare_outputs(ans_out, user_out):
    ans = ans_out.split('\n')
    user = user_out.split('\n')

    return sorted(ans) == sorted(user)

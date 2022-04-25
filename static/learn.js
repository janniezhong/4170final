let currLine = "";

let currLesson = {
    "chapter": "This is the current chapter",
    "chapter_id": "0",
    "lesson_id": "0",
    "topic": "This is the topic",
    "prompt": "This is the prompt.",
    "feedback": "This is the feedback",
    "instruction": "This is the instruction",
    "answer": "This is the answer",
    "response": "This is the response",
    "previous_lesson_id": "0",
    "next_lesson_id": "1",
}

let lessonFinished = false

var term;

function checkAnswer(){

    if (currLine == currLesson["answer"]){ // if the answer is correct
        getNextLesson()
    } else {
        term.write(" \r\n > That wasn't quite right :/ Try again? \r\n > ")
    }

    currLine = "" // clear line
}

function getNextLesson(){ // if the lesson is the last one, go to the quiz instead

    data = {
        "id": currLesson["next_lesson_id"],
        "response": currLine
    }
    $.ajax({
        type: "POST",
        url: "/next_lesson",                
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify(data),
        success: function(result){
            console.log("success!")
            console.log(result)

            currLesson["chapter"] = result["chapter"]
            currLesson["chapter_id"] = result["chapter_id"]
            currLesson["lesson_id"] = result["lesson_id"]
            currLesson["topic"] = result["topic"]
            currLesson["prompt"] = result["prompt"]
            currLesson["feedback"] = result["feedback"]
            currLesson["instruction"] = result["instruction"]
            currLesson["answer"] = result["answer"]
            currLesson["response"] = result["response"]
            currLesson["previous_lesson_id"] = result["previous_lesson_id"]
            currLesson["next_lesson_id"] = result["next_lesson_id"]
            updateTerminal(currLesson["response"])
            if (currLesson["lesson_id"] == "final"){
                lessonFinished = true
            }
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }
    });
}

function updateTerminal(s){
    term.write('\r\n')
    term.write(s)
    term.write('\r\n > ')
}

$(document).ready(function(){
    term = new Terminal({cursorBlink: "block"});
    term.open(document.getElementById('terminal'));
    term.write('Hi! \r\n')

    getNextLesson()

    term.onKey(e => {
        let code  = e.key.charCodeAt()

        if (code == 13){
            if (lessonFinished){
                window.location.href = "/quiz/1"
            } else if (currLine) {
                checkAnswer()
            }
        } else if (code < 32) { // Control
            return;
        } else if (code == 127 || code == 8){
            if (currLine) {
                currLine = currLine.slice(0, currLine.length - 1);
                term.write("\b \b");
            }
        } else {
            currLine += e.key;
            term.write(e.key);
        }

    })

    $("#pdid").progressbar({
        value:20
    });
}) 
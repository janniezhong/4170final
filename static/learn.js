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

function updateCurrLesson(lesson_info){
    currLesson["chapter"] = lesson_info["chapter"]
    currLesson["chapter_id"] = lesson_info["chapter_id"]
    currLesson["lesson_id"] = lesson_info["lesson_id"]
    currLesson["topic"] = lesson_info["topic"]
    currLesson["prompt"] = lesson_info["prompt"]
    currLesson["feedback"] = lesson_info["feedback"]
    currLesson["instruction"] = lesson_info["instruction"]
    currLesson["answer"] = lesson_info["answer"]
    currLesson["response"] = lesson_info["response"]
    currLesson["previous_lesson_id"] = lesson_info["previous_lesson_id"]
    currLesson["next_lesson_id"] = lesson_info["next_lesson_id"]
}

function displayCurrLesson(){
    // display title
    $(".title").empty()
    console.log(currLesson["topic"])
    $(".title").text(currLesson["topic"])

    // display prompt
    $(".prompt").empty()
    $(".prompt").text(currLesson["prompt"])

    // display instruction
    $(".instruction").empty()
    $(".instruction").text(currLesson["instruction"])

    $("#prev").attr("href", "/learn/"+currLesson["previous_lesson_id"])

}

function checkAnswer(){ // if the lesson is the last one, go to the quiz instead

    data = {
        "id": currLesson["lesson_id"],
        "response": currLine
    }
    $.ajax({
        type: "POST",
        url: "/check_answer",                
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify(data),
        success: function(result){
            console.log("success!")
            console.log(result)
            let correct = result["correct"]
            let error = result["error"]
            if (correct == "true"){
                updateTerminal(currLesson["response"])
                finishLesson()
            } else {
                updateTerminal(error)
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
function finishLesson(){

    // pop up modal
    $("#modal-button").trigger("click")
    $(".modal-body").empty()
    $(".modal-body").text(currLesson["feedback"])

    // allow next button
    if (currLesson["lesson_id"] == "final"){
        $("#next").attr("href", "/quiz/1")
    } else {
        $("#next").attr("href", "/learn/"+currLesson["next_lesson_id"])
    }

    // disallow typing in terminal
    // term.onKey(e => {})
}

function updateTerminal(s){
    term.write('\r\n')
    term.write(s)
    term.write('\r\n> ')
}

$(document).ready(function(){
    term = new Terminal({cursorBlink: "block", cols: 50, rows: 22, theme: {
        background: '#8d8b8bff'
      }});
    term.open(document.getElementById('terminal'));
    term.write("> ")
    console.log(lesson_info)

    updateCurrLesson(lesson_info)
    displayCurrLesson()


    term.onKey(e => {
        let code  = e.key.charCodeAt()

        if (code == 13){
            if (lessonFinished){
                window.location.href = "/quiz/1"
            } else if (currLine) {
                checkAnswer()
                currLine=""
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
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
    if (currLesson["lesson_id"] == "final"){
        $("#next").attr("href", "/quiz/1")
    } else {
        $("#next").attr("href", "/learn/"+currLesson["next_lesson_id"])
    }
}

function checkAnswer(){

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

    $("#feedback").empty()
    $("#feedback").append(currLesson["feedback"])

    // disallow typing in terminal
    // term.onKey(e => {})
}

function updateTerminal(s){
    term.write('\r\n')
    term.write(s)
    term.write('\r\n> ')
}

function setProgBar(id) {
    var elem = document.getElementById("lesson-prog-bar");
    var val = Math.round(100/14 * (parseInt(id)-1));
    console.log(val)
    elem.setAttribute("style", "width: " + val.toString() + "%;");
    elem.setAttribute("aria-valuenow", val.toString());
  
    $("#lesson-prog-bar").text(val + "%");
  }

  let els = document.getElementsByClassName('step');
  let steps = [];
  
  function progress(stepNum) {
    let p = stepNum * 15;
    document.getElementsByClassName('percent_1')[0].style.width = `${p}%`;
    document.getElementsByClassName('percent_2')[0].style.width = `${p}%`;
    steps.forEach((e) => {
      if (e.id <= stepNum) {
        e.classList.add('completed');
      }
      if (e.id > stepNum) {
        e.classList.remove('selected', 'completed');
      }
    });
  }


$(document).ready(function(){
    term = new Terminal({cursorBlink: "block", cols: 75, rows: 13, fontSize: 13,theme: {
        background: '#8d8b8bff',
      }});
    term.open(document.getElementById('terminal'));
    term.write("> ")
    console.log(lesson_info)

    updateCurrLesson(lesson_info)
    displayCurrLesson()
    if (currLesson["lesson_id"] == "final"){
        setProgBar("14")
    } else {
        setProgBar(currLesson["lesson_id"])
    }

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

}) 

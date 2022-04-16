let currLine = "";

let currLesson = {
    "lesson_id": "0",
    "title": "this is the title",
    "text": "this is the prompt",
    "answer": "this is the correct answer",
    "next_lesson_id": "1"
}

var term;

function checkAnswer(){
    if (true){ // if the answer is correct
        getNextLesson()
        currLine = "" // clear line
    } else {
        //error handling
    }

}

function getNextLesson(){
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
        
            currLesson["lesson_id"] = result["lesson_id"]
            currLesson["title"] = result["title"]
            currLesson["text"] = result["text"]
            currLesson["answer"] = result["answer"]
            currLesson["next_lesson_id"] = result["next_lesson_id"]
            console.log(currLesson["text"])
            updateTerminal(currLesson["text"])
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
    term.write(s)
    term.write('\r\n > ')

}

$(document).ready(function(){
    term = new Terminal({cursorBlink: "block"});
    term.open(document.getElementById('terminal'));
    term.write('Hi! \r\n > ')

    getNextLesson()

    term.onKey(e => {
        console.log(e.key);
        let code  = e.key.charCodeAt()

        if (code == 13){
            if (currLine) {
                term.write("\n\r > ");
                checkAnswer()
            }
        } else if (code < 32 || code == 127) { // Control
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
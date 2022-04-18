var term;

function checkAnswer(currLine, qid){
    if (currLine == "testing"){ // if the answer is correct
        getNextPage(qid)
    } else {
        term.write(" \r\n > That wasn't quite right :/ Try again? \r\n > ")
    }

    currLine = "" // clear line
}

function getNextPage(qid){ // if the lesson is the last one, go to the quiz instead
    if (qid == 4) {
        window.location.pathname = '/quiz/result'
    } else {
        window.location.pathname = '/quiz/' + (qid + 1).toString()
    }
}

function updateTerminal(s){
    term.write(s)
    term.write('\r\n > ')
}

function createHeader() {
    let hline = "-".repeat(80);
    let vline = "|" + " ".repeat(78) + "|"
    let title = "|" + " ".repeat(26) + "Searching Through Recipes" + " ".repeat(27) + "|"

    const arr = [hline, vline, vline, title, vline, vline, hline]

    return arr.join("\r\n")
}

function getCurrQuizNum() {
    return window.location.href.trim().slice(-1)
}

$(document).ready(function(){
    term = new Terminal({cursorBlink: "block"});

    term.write(createHeader());

    term.open(document.getElementById('terminal'));
    
    term.write(quiz_info["instruction"] + "\r\n\r\n\r\n")
    term.write(quiz_info["question"] + "\r\n\r\n\r\n")

    updateTerminal("");

    var currLine = ""

    term.onKey(e => {
        let code  = e.key.charCodeAt()

        if (code == 13){
            if (currLine) {
                checkAnswer(currLine, parseInt(getCurrQuizNum()))
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

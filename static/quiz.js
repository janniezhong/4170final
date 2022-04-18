
var term;
let currLine = "";
function checkAnswer(){
    if (currLine == "testing"){ // if the answer is correct
        getNextQuiz()
    } else {
        term.write(" \r\n > That wasn't quite right :/ Try again? \r\n > ")
    }

    currLine = "" // clear line
}

function getNextQuiz(){ // if the lesson is the last one, go to the quiz instead
    window.location.pathname = '/quiz/2'
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

function getNextQuiz(quizId) {

    
    switch (quizId) {
        case "1":
          
            return {
                "question": "\r\nPerson 1: My favorite condiments are ketchup and mustard. I’d like to find the names of recipes containing these ingredients in this recipe book.\r\n",
                "answer": "testing"
            }
        case "2":
            return {
                "question": "\r\nPerson 2: I love salty food, especially things made with soy sauce. I’d like to find the names of recipes containing the words “salt” or “soy sauce” from this recipe book.\r\n",
                "answer": "testing"
            }
        case "3":
            return {
                "question": "\r\nPerson 3: I’m interested in Recipe3 in this book. Unfortunately, I don’t have a Dutch oven: can you search Recipe3 for the phrase “dutch oven” (case insensitive), so I know whether it’s essential or not?\r\n",
                "answer": "testing"
            }
        case "4":
            return {
                "question": "\r\nPerson 4: I love galettes, both savory and sweet. I’d like to find the names of all recipes that are making galettes in this book.\r\n",
                "answer": "testing"
            }
        default:
            return null
    }
}

function getCurrQuizNum() {
    return window.location.href.trim().slice(-1)
}

$(document).ready(function(){
    term = new Terminal({cursorBlink: "block"});

    term.write(createHeader());

    term.open(document.getElementById('terminal'));
    
    let currQuiz = getNextQuiz(getCurrQuizNum());

    term.write( currQuiz["question"] )

    updateTerminal("");



    term.onKey(e => {
        let code  = e.key.charCodeAt()

        if (code == 13){
            if (currLine) {
                console.log(currLine)
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

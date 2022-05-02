var term;

var container = {
    currLine: "",
    keyboardContent: ""
};

function checkAnswer(currLine, qid) {
    data = {
        id: qid,
        response: currLine,
    };

    console.log(currLine);

    $.ajax({
        type: "POST",
        url: "/save_response",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(data),
        success: function (result) {
            let res = result[qid];

            if (res == 1) {
                $("#next").attr("href", getNextPage(qid));
                term.write("\r\n Nice! Click next to go to the next page!\r\n");
            } else {
                term.write("\r\n That wasn't quite right :/ Try again? \r\n > ");
            }
        },
        error: function (request, status, error) {
            console.log("Error");
            console.log(request);
            console.log(status);
            console.log(error);
        },
    });
}

function getPrevPage(qid) {
    if (qid == 1) {
        return "/learn/final";
    } else {
        return "/quiz/" + (qid - 1).toString();
    }
}

function getNextPage(qid) {
    // if the lesson is the last one, go to the quiz instead
    if (qid == 4) {
        return "/quiz/result";
    } else {
        return "/quiz/" + (qid + 1).toString();
    }
}

function updateTerminal(s) {
    term.write(s);
    term.write("\r\n > ");
}

function createHeader() {
    let hline = "-".repeat(80);
    let vline = "|" + " ".repeat(78) + "|";
    let title =
        "|" + " ".repeat(26) + "Searching Through Recipes" + " ".repeat(27) + "|";

    const arr = [hline, vline, vline, title, vline, vline, hline];

    return arr.join("\r\n");
}

function getCurrQuizNum() {
    return window.location.href.trim().slice(-1);
}

function renderTreeOne() {
    term.write("recipe_book \r\n");
    term.write("├── recipe1 \r\n");
    term.write("├── recipe2 \r\n");
    term.write("├── recipe3 \r\n");
    term.write("└── recipe4 \r\n");

    term.write("0 directories, 4 files");

    // $( ".instruction" ).empty();

    // $('<p>' + "recipe_book \r\n"+"├── recipe1 \r\n"+"├── recipe2 \r\n"+ "├── recipe3 \r\n"+"└── recipe4 \r\n"+ '</p>').appendTo('.instruction');
}

function renderTreeTwo() {
    term.write("recipe_book \r\n");
    term.write("├── savory \r\n");
    term.write("│   ├── recipe1\r\n");
    term.write("│   └── recipe2\r\n");
    term.write("└── sweet\r\n");
    term.write("    ├── recipe3\r\n");
    term.write("    └── recipe4\r\n");

    term.write("2 directories, 4 files");

    // $( ".instruction" ).empty();

    // $('<p>' + "recipe_book \r\n"+"├── savory \r\n"+"│   ├── recipe1\r\n"+ "│   └── recipe2\r\n"+"└── sweet\r\n"+"    ├── recipe3\r\n"+"    └── recipe4\r\n"+ '</p>').appendTo('.instruction');
}

function renderTree(qid) {
    switch (qid) {
        case 1:
        case 2:
        case 3:
            renderTreeOne();
            return;
        case 4:
            renderTreeTwo();
        default:
            return;
    }
}
function addText() {
    $(".prompt").empty();
    $("<p>" + quiz_info["instruction"] + "</p>").appendTo(".prompt");
    $("<p>" + "\r\n\r\n" + "</p>").appendTo(".prompt");

    $("<p>" + quiz_info["question"] + "</p>").appendTo(".prompt");
}

function addTitle(pid) {
    $(".title").empty();
    $("<p>" + "Quiz " + pid + "</p>").appendTo(".title");
}

function setProgBar(qid) {
    var elem = document.getElementById("quiz-prog-bar");
    var val = 25 * (qid - 1);
    elem.setAttribute("style", "width: " + val.toString() + "%;");
    elem.setAttribute("aria-valuenow", val.toString());

    $("#quiz-prog-bar").text(val + "%");
}

function getContentFromClipboard() {
    navigator.clipboard
        .readText()
        .then((copiedText) => {
            container.keyboardContent = copiedText;
        });
}

function putContentToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        console.log("into clipboard now")
    }, () => {
        console.log("rejected bro")
    });
}

$(document).ready(function () {
    addText();

    term = new Terminal({
        cursorBlink: "block",
        cols: 50,
        rows: 22,
        theme: {
            background: "#8d8b8bff",
        },
    });

    term.open(document.getElementById("terminal"));

    var qidNum = parseInt(getCurrQuizNum());

    addTitle(qidNum);
    renderTree(qidNum);
    setProgBar(qidNum);

    updateTerminal("");

    $("#prev").attr("href", getPrevPage(qidNum));

    term.attachCustomKeyEventHandler((arg) => {
        getContentFromClipboard();

        if (arg.ctrlKey && arg.code === "KeyC" && arg.type === "keydown") {
            const selection = term.getSelection();
            if (selection) {
                putContentToClipboard(selection);
                return false;
            }
        }

        if (arg.ctrlKey && arg.code === "KeyV" && arg.type === "keydown") {
            term.write(container.keyboardContent);
            container.currLine = container.keyboardContent;
            return false;
        }

        return true;
    });

    term.onKey((e) => {
        let code = e.key.charCodeAt();

        getContentFromClipboard();

        if (e.key == "KeyV" && e.key.ctrlKey) {
            this.write(keyboardContent)
            container.currLine += keyboardContent
            return;
        }

        if (code == 13) {
            if (container.currLine) {
                checkAnswer(container.currLine, qidNum);
                container.currLine = "";
            }
        } else if (code < 32) {
            // Control
            return;
        } else if (code == 127 || code == 8) {
            if (container.currLine) {
                container.currLine = container.currLine.slice(
                    0,
                    container.currLine.length - 1
                );
                term.write("\b \b");
            }
        } else {
            container.currLine += e.key;
            term.write(e.key);
        }
    });
});

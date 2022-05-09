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

    $.ajax({
        type: "POST",
        url: "/save_response",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(data),
        success: function (result) {
            var flgCorrect = result["flgCorrect"];
            var errMsg = result["errMsg"];

            if (flgCorrect) {
                $("#next").attr("href", getNextPage(qid));
                term.write("\r\n Nice! Click next to go to the next page!\r\n > ");
            } else {
                term.write("\r\n That wasn't quite right :/ Try again? Some hints:\r\n \x1b[1;31m" + errMsg + " \x1b[0;97m\r\n > ");
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
        return "/result";
    } else {
        return "/quiz/" + (qid + 1).toString();
    }
}

// https://stackoverflow.com/a/13348618
function isChrome() {
    var isChromium = window.chrome;
    var winNav = window.navigator;
    var vendorName = winNav.vendor;
    var isOpera = typeof window.opr !== "undefined";
    var isIEedge = winNav.userAgent.indexOf("Edg") > -1;
    var isIOSChrome = winNav.userAgent.match("CriOS");

    if (isIOSChrome) {
        return false
    } else if (
        isChromium !== null &&
        typeof isChromium !== "undefined" &&
        vendorName === "Google Inc." &&
        isOpera === false &&
        isIEedge === false
    ) {
       return true
    } else {
        return false
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
    // $("<p>" + quiz_info["instruction"] + "</p>").appendTo(".prompt");
    // $("<p>" + "\r\n\r\n" + "</p>").appendTo(".prompt");

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
    if (!isChrome()) {
        return
    }

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
        cursorBlink: "block", cols: 80, rows: 13, fontSize: 12, theme: {
            background: '#434343ff'
        }
    });

    term.open(document.getElementById("terminal"));
    term.write("> ")

    var qidNum = parseInt(getCurrQuizNum());

    addTitle(qidNum);
    renderTree(qidNum);
    setProgBar(qidNum);

    updateTerminal("");

    $("#prev").attr("href", getPrevPage(qidNum));
    $("#next").attr("href", getNextPage(qidNum));

    term.attachCustomKeyEventHandler((arg) => {
        getContentFromClipboard();

        if ((arg.ctrlKey || arg.metaKey) && arg.code === "KeyC" && arg.type === "keydown") {
            if (!isChrome()) {
                alert("copy/paste from terminal is only supported on Google Chrome")
                return true;
            }

            const selection = term.getSelection();
            if (selection) {
                putContentToClipboard(selection);
                return false;
            }
        }

        if ((arg.ctrlKey || arg.metaKey) && arg.code === "KeyV" && arg.type === "keydown") {
            if (!isChrome()) {
                alert("copy/paste from terminal is only supported on Google Chrome")
                return true;
            }

            term.write(container.keyboardContent);
            container.currLine = container.keyboardContent;
            return false;
        }

        return true;
    });

    term.onKey((e) => {
        let code = e.key.charCodeAt();

        if (code == 13) {
            if (container.currLine) {
                checkAnswer(container.currLine, qidNum);
                container.currLine = "";
            }
        } else if (code < 32) {
            // Control
            return
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

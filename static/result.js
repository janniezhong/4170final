var term;

function updateTerminal(s){
    term.write(s)
    term.write('\r\n > ')
}

function printCongrats() {
    var spaces = " ".repeat(20)
    term.write("\r\n\r\n\r\n" + spaces + "                                 _\r\n")       
    term.write(spaces + "  ___ ___  _ __   __ _ _ __ __ _| |_ ___\r\n") 
    term.write(spaces + " / __/ _ \\| '_ \\ / _` | '__/ _` | __/ __|\r\n")
    term.write(spaces + "| (_| (_) | | | | (_| | | | (_| | |_\\__ \\\r\n")
    term.write(spaces + " \\___\\___/|_| |_|\\__, |_|  \\__,_|\\__|___/\r\n")
    term.write(spaces + "                 |___/  \r\n")
}

$(document).ready(function(){
    term = new Terminal({
        cursorBlink: "block",
        cols: 120,
        rows: 30,
        theme: {
          background: "#8d8b8bff",
        },
      });

    printCongrats();

    $("#prev").attr("href",  "/quiz/4")

    term.open(document.getElementById('terminal'));

    term.write("\r\n  score=" + score.toString() + "\r\n")
    term.write("\r\n  Congratulations! You’ve successfully completed this tutorial. Now go forth and grep!\r\n\r\n")
    term.write("\r\n\r\n  For more resources on grep, check out:")
    term.write("\r\n         - the grep man page")
    term.write("\r\n         - using regex with grep")
    term.write("\r\n         - variants of grep (egrep, fgrep)")
}) 

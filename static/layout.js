let navBarInfo = {
    "numLessons": 0,
    "numQuizzes": 0
}

function loadNavBar(){
    $("#learnSubmenu").empty()
    $("#quizSubmenu").empty()

    for (let i = 1; i< navBarInfo["numLessons"]; i++){
        let newItem = $("<li>");
        let newLink = $("<a href='/learn/" + i+"'> lesson " + i + " </a>")
        $(newItem).append(newLink)
        $("#learnSubmenu").append(newItem)
    }
    let newItem = $("<li>");
    let newLink = $("<a href='/learn/final'> lesson " + navBarInfo["numLessons"] + " </a>")
    $(newItem).append(newLink)
    $("#learnSubmenu").append(newItem)


    for (let i = 1; i<= navBarInfo["numQuizzes"]; i++){
        let newItem = $("<li>");
        let newLink = $("<a href='/quiz/" + i+"'> quiz " + i + " </a>")
        $(newItem).append(newLink)
        $("#quizSubmenu").append(newItem)
    }

}

$(document).ready(function(){
    navBarInfo["numLessons"] = navbar_info["num_lessons"]
    navBarInfo["numQuizzes"] = navbar_info["num_quizzes"]

    loadNavBar()
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
        $(this).toggleClass('active');
    });
})
$(document).ready(function () {
    $.ajax({
        url: "/executerList",
        success: function (data) {

            for (var i = 0; i < data.executer.length; i++) {
                systemSelect = document.getElementById('executer');
                systemSelect.options[systemSelect.options.length] = new Option(data.executer[i], data.executer_code[i]);

            }

        }
    });
});
// ****************************************************************************************************************
$(document).ready(function () {
    $.ajax({
        url: "/subjectList",
        success: function (data) {

            for (var i = 0; i < data.subjectList.length; i++) {
                systemSelect = document.getElementById('subject');
                systemSelect.options[systemSelect.options.length] = new Option(data.subjectList[i], data.subject_code[i]);

            }

        }
    });
});

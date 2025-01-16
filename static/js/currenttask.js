$(document).ready(function () {
    $.ajax({
        url: "/executerList",
        success: function (data) {

            for (var i = 0; i < data.executer.length; i++) {
                systemSelect = document.getElementById('executer_srch');
                systemSelect.options[systemSelect.options.length] = new Option(data.executer[i], data.executer_code[i]);

            }

        }
    });
});
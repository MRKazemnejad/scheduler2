
$(document).ready(function () {
    $.ajax({
        url: "/numericdata",
        success: function (data) {
            document.getElementById('total_count').innerText=data.count;
            document.getElementById('total_done').innerText=data.done;
            document.getElementById('total_current').innerText=data.active;
        }
    });
});
// ****************************************************************************************************************

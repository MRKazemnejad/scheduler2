
function loadimages(id) {

    var exe_code = id

    $.ajax({

        url: "/loadimages",
        data: {
            'id': JSON.stringify(exe_code),
        },
        success: function (data) {

            if (data.images.length == 0) {
                // $('.imageclass').remove();
                // $('<div class="carousel-item h-90"></div>').appendTo('.carousel-inner');
            } else {

                for (let j = 0; j < data.images.length; j++) {
                    $('<div class="carousel-item"><img src=' + data.images[j].url + ' class=" mx-auto d-block w-80 imageclass" alt="HTML">   </div>').appendTo('.carousel-inner');
                    // $('<li class="imageclass" data-target="#carousel" data-slide-to="' + j + '"></li>').appendTo('.carousel-indicators')

                }
                $('.carousel-item').first().addClass('active');
                // $('.carousel-indicators > li').first().addClass('active');
                // $('#carousel').carousel();

            }
        }
    });


}

function clearimg() {
   $('.carousel-item').remove()
}


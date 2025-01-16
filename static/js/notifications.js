$(document).ready(function () {
    $.ajax({
        url: "/notification",
        success: function (data) {

            setMessage(data);

        }
    });
});


function setMessage(message) {

    document.getElementById('bellCount').setAttribute('data-count', 0);

    for (let i = 0; i <= message.notif.length; i++) {


        // var is_show = message['message'][i]['is_showed']
        var is_read = message.notif[i]['is_read']
        //
        if (is_read == false) {


            //create img

            // var img=document.createElement('img')
            // img.className='rounded-circle';
            // img.setAttribute('src','/static/img/user.jpg"')
            // img.setAttribute('width','40')
            // img.setAttribute('height','40')

            //create div
            var div = document.createElement('div')
            div.className = 'kazem-align-currenttask account';

            // var div2 = document.createElement('div')
            // div2.className = 'ms-4';

            //create new element divider
            var divider = document.createElement('hr')
            divider.className='dropdown-divider';

            var d = new Date(message.notif[i]['notif_date']); /*making iran time zone*/
            var result2 = new Date(d.toISOString()).toLocaleString('fa-IR');/*making persian calender*/

            // Create a new anchor element
            var newtag = document.createElement('small');
            newtag.textContent =result2

            var newAnchor = document.createElement('a');
            newAnchor.className = 'dropdown-item ';
            var id = message.notif[i]['notif_code_id'];
            newAnchor.setAttribute('id', id)
            newAnchor.href = '/notification_details/' + id;
            //
            //show all
             var newAnchor1 = document.createElement('a');
            newAnchor1.className = 'dropdown-item';
            newAnchor1.href = '/notifications/';
            //show all h

             var newh1 = document.createElement('h6')
            newh1.className = 'fw-normal mb-0';
            newh1.textContent = 'نمایش همه';


            // message_text=message.notif[i]['notif']+" : "+message['message'][i]['diesel_name']
            message_text=message.notif[i]['notif']

            var newh = document.createElement('h6')
            newh.className = 'fw-normal mb-0';
            newh.textContent = message_text;
            //
            //
            // Append the anchor element to the li element
            // newAnchor.appendChild(img)
            newAnchor.appendChild(newh)
            newAnchor.appendChild(newtag)
            div.appendChild(newAnchor)





            // // Get the ul element with the id "notify"
            var ulElement = document.getElementById('notify');
            //
            // Append the new li element to the ul element
            ulElement.appendChild(div);
            ulElement.appendChild(divider)

            if((i+1) == message.notif.length){

                ulElement.appendChild(divider)
                newAnchor1.appendChild(newh1)
                div.appendChild(newAnchor1)
                ulElement.appendChild(div);
            }
            //
            // getting object of count
            count = document.getElementById('bellCount').getAttribute('data-count');
            //
            document.getElementById('bellCount').setAttribute('data-count', parseInt(count) + 1);

        }


    }


}







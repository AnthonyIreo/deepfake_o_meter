/* //if the message form input is empty
function message_form_submit(){
    var message_name = $("#message_name").val();
    var message_email = $("#message_email").val();
    var message_subject = $("#message_subject").val();
    var message = $("#message_message").val();


    if (message_name == ''){
        alert("please enter your name.");
    }
    else if (message_email == ''){
        alert("please enter your email.");
    }
    else if (message_subject == ''){
        alert("please enter a subject.");
    }
    else if (message == ''){
        alert("please enter your message.");
    };
}

 */
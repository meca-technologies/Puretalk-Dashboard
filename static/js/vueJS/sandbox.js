var sandbox_messages = new Vue({
    delimiters: ['[[', ']]'],
    el: '#twilio-sandbox-body',
    data: {
        messages:[]
    }
})

$(".nav-item").click(function(){
    var nav_items = document.getElementsByClassName("nav-item");
    for(var i = 0; i<nav_items.length; i++){
        $(nav_items[i]).removeClass("active-light");
    }
    $(this).addClass("active-light");
});

var current_call_sid;

$("#sandbox-call-now").click(function(){
    var selected_camp = $(".active-light")[0];
    var post_data = {
        "phone_number":$("#sandbox-phone-number").val(),
        "campaign":$(selected_camp).attr("campaign-id")
    }
    console.log(post_data)
    sandbox_messages.messages = [];
    var url = '/api/v1/twilio/sandbox/make_call';
    $.ajax({
        type: 'POST',
        url: url,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: JSON.stringify(post_data),
        success: function(data){
            console.log("data");
            console.log(data);
            if(data['Message'] == 'Success'){
                call_id = data['call_sid']
                alerts.alerts.push({
                    "status":"success",
                    "message":"Update was successful"
                })
                current_call_sid = call_id;
                getConversation(call_id);
            }
            else{
                alerts.alerts.push({
                    "status":"danger",
                    "message":"Failed to save"
                })
            }
        },
        error: function(data){
            console.log('FAILURE');
        }
    });
})

var sidebar_toggler = $(".sidenav-toggler")[0];
$(sidebar_toggler).removeClass("d-xl-none");

function getConversation(call_id){
    var getConvoInt = setInterval(function(){
        if(call_id == current_call_sid){
            var url = '/api/v1/twilio/sandbox/make_call?call_id='+call_id;
            var jqxhr = $.get( url, function(data) {
                sandbox_messages.messages = data['conversation'];
                $("#chat-holder").scrollTop($("#chat-holder")[0].scrollHeight);
            })
        }
        else{
            clearInterval(getConvoInt);
        }
    }, 5000)
}
var notifications = new Vue({
    delimiters: ['[[', ']]'],
    el: '#notification-body',
    data: {
        notifications:{},
        length:0
    }
})

function updateNotification(){
    var jqxhr = $.get( '/api/v1/companies/first-time', function(data) {
        console.log(data);
        var length = 0;
        var pop_up = true;
        if(data['form_length'] == 0){
            length += 1;
            if(window.location.pathname == '/form-builder'){
                pop_up = false;
            }
        }
        else if(data['campaign_length'] == 0){
            length += 1;
            if(window.location.pathname == '/campaigns'){
                pop_up = false;
            }
        }
        else if(data['lead_length'] == 0){
            length += 1;
            if(window.location.pathname == '/import-leads'){
                pop_up = false;
            }
        }
        notifications.notifications = data;
        notifications.length = length;
        if(length > 0 && pop_up){
            if($("#notif-badge").parent().attr("aria-expanded") == 'false'){
                $("#notif-badge").click();
            }
        }
        document.getElementById("notif-badge").style.display = '';
    });
}

updateNotification();
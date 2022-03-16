var thisCompanyID;
var twilioSettings = new Vue({
    delimiters: ['[[', ']]'],
    el: '#twilio-body',
    data: {
        twilio:[
            {
              "created_at": "Tue, 10 Aug 2021 18:54:03 GMT", 
              "inbound_recording": "record-from-answer", 
              "number": "", 
              "outbound_recording": "record-from-answer", 
              "updated_at": "Tue, 10 Aug 2021 18:55:23 GMT",
              "twilio_account_sid": [""],
              "twilio_application_sid": "",
              "twilio_auth_token": [""],
              "twilio_enabled": [false],
            }
        ],
        vici:{
            "vici_enabled":false,
            "vici_server":"",
            "vici_user":"",
            "vici_password":""
        }
    }
})

$('body').on('click','.twilio-edit', function(){
    console.log($(this).attr("company-id"));
    thisCompanyID = $(this).attr("company-id")
    updateTwilio($(this).attr("company-id"));
    updateVici();
});

function updateVici(){
    var url = '/api/v1/companies?companyid='+thisCompanyID;
    console.log(url);
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        try{
            twilioSettings.vici['vici_enabled'] = data[0]['vici_enabled'];
            twilioSettings.vici['vici_server'] = data[0]['vici_server'];
            twilioSettings.vici['vici_user'] = data[0]['vici_user'];
            twilioSettings.vici['vici_password'] = data[0]['vici_password'];
        }catch(error){
            twilioSettings.vici['vici_enabled'] = false;
            twilioSettings.vici['vici_server'] = '';
            twilioSettings.vici['vici_user'] = '';
            twilioSettings.vici['vici_password'] = '';
        }
        setTimeout(function(){
            var viciBodies = $('.show_hide_vici_fields');
            if(document.getElementById("viciEnabled").checked){
                for(var i = 0; i<viciBodies.length; i++){
                    $(viciBodies[i]).show(500);
                }
            }
            else{
                for(var i = 0; i<viciBodies.length; i++){
                    $(viciBodies[i]).hide(500);
                }
            }
        },1000)
    })
}

function updateTwilio(){
    var url = '/api/v1/twilio?limit=2000';
    try{
        url += '&companyid='+thisCompanyID;
    }catch(error){}
    console.log(url);
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        twilioSettings.twilio = data;
        setTimeout(function(){
            var twilioBodies = $('.show_hide_twilio_fields');
            if(document.getElementById("twilioEnabled").checked){
                for(var i = 0; i<twilioBodies.length; i++){
                    $(twilioBodies[i]).show(500);
                }
            }
            else{
                for(var i = 0; i<twilioBodies.length; i++){
                    $(twilioBodies[i]).hide(500);
                }
            }
        },1000)
    })
}

$('body').on('click','#twilioEnabled', function(){
    var twilioBodies = $('.show_hide_twilio_fields');
    console.log('Check Twilio Enabled');
    console.log(this.checked);
    if(this.checked){
        for(var i = 0; i<twilioBodies.length; i++){
            $(twilioBodies[i]).show(500);
        }
    }
    else{
        for(var i = 0; i<twilioBodies.length; i++){
            $(twilioBodies[i]).hide(500);
        }
    }
})

$('body').on('click','#viciEnabled', function(){
    var viciBodies = $('.show_hide_vici_fields');
    console.log('Check Twilio Enabled');
    console.log(this.checked);
    if(this.checked){
        for(var i = 0; i<viciBodies.length; i++){
            $(viciBodies[i]).show(500);
        }
    }
    else{
        for(var i = 0; i<viciBodies.length; i++){
            $(viciBodies[i]).hide(500);
        }
    }
})

$('body').on('click','#save-twilio-number', function(){
    var updateData = {
        "company_id":thisCompanyID,
        "id":$("#twilio-number-id").val(),
        "inbound_recording":$("#twilio-number-inbound").val(),
        "number":$("#twilio-number-phone").val(),
        "outbound_recording":$("#twilio-number-outbound").val()
    }
    console.log(updateData);
    postToAPI('/api/v1/twilio', updateData, 'POST', 'updateTwilio');
})

$('body').on('click','#save-twilio-info', function(){
    var updateData = {
        "id":thisCompanyID,
        "twilio_enabled":document.getElementById("twilioEnabled").checked?true:false,
        "twilio_account_sid":$("#twilio-account-sid").val(),
        "twilio_auth_token":$("#twilio-auth-token").val(),
        "twilio_application_sid":$("#twilio-application-sid").val(),
        "twilio_profile_sid":$("#twilio-profile-sid").val()
    }
    console.log(updateData)
    postToAPI('/api/v1/companies', updateData, 'PUT', 'updateTwilio');
})

$('body').on('click','#save-vici-info', function(){
    var updateData = {
        "id":thisCompanyID,
        "vici_enabled":document.getElementById("viciEnabled").checked?true:false,
        "vici_server":$("#vici-server").val(),
        "vici_user":$("#vici-user").val(),
        "vici_password":$("#vici-password").val()
    }
    console.log(updateData)
    postToAPI('/api/v1/companies', updateData, 'PUT', 'doNothing');
})
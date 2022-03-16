var emailSettings = new Vue({
    delimiters: ['[[', ']]'],
    el: '#email-body',
    data: {
        email:[
            {
                "mail_driver": "smtp",
                "mail_encryption": "tls",
                "mail_from_email": "",
                "mail_from_name": "",
                "mail_host": "smtp.gmail.com",
                "mail_password": "password",
                "mail_port": "587",
                "mail_username": "",
                "verified": false
            }
          ]
    }
})

function updateEmailSettings(){
    var url = '/api/v1/email?limit=2000';
    try{
        url += '&companyid='+thisCompanyID;
    }catch(error){}
    console.log(url);
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        emailSettings.email = data;
    })
}

updateEmailSettings();

$('body').on('click','#save-email-settings', function(){
    var updateData = {
        "id":$("#mail_id").val(),
        "mail_driver":document.getElementById("mail_driver_smtp_checkbox").checked?'smtp':'mail',
        "mail_encryption":$("#mail_encryption").val(),
        "mail_from_email":$("#mail_from_email").val(),
        "mail_from_name":$("#mail_from_name").val(),
        "mail_host":$("#mail_host").val(),
        "mail_password":$("#mail_password").val(),
        "mail_port":$("#mail_port").val(),
        "mail_username":$("#mail_username").val()
    }
    console.log(updateData)
    postToAPI('/api/v1/email', updateData, 'PUT', 'updateEmailSettings');
})
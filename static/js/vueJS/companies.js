try{
    document.getElementById('company-body-loading').style.display = '';
    document.getElementById('company-body').style.display = 'none';
}catch(error){}
var companyTable;
var companyID;

try{
    sortColumn = $('#company-body').attr('sort-col');
}catch(error){
    sortColumn = 1
}

try{
    sortStyle = $('#company-body').attr('sort-style');
}catch(error){
    sortStyle = 'asc';
}

try{
    pageLength = $('#company-body').attr('page-length');
}catch(error){
    pageLength = 5;
}

try{
    hideColsRaw = $('#company-body').attr('hide-col');
    hideCols = hideColsRaw.split(',');
}catch(error){
    hideCols = [];
}

var companies = new Vue({
    delimiters: ['[[', ']]'],
    el: '#company-body',
    data: {
        companies:[]
    }
})
var companyDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#company-edit',
    data: {
        details:{
            "address": "", 
            "app_layout": "sidebar", 
            "billing": {
              "charge_amount": "0.07", 
              "charge_type": 0, 
              "company_id": "613b8a775a2cd24ac1a33b26"
            }, 
            "card_brand": null, 
            "card_last_four": null, 
            "created_at": "2020-09-10 16:43:22", 
            "email": "samz@hscwarranty.com", 
            "id": "613b8a775a2cd24ac1a33b26", 
            "licence_expire_on": "2020-11-10", 
            "locale": "en", 
            "logo": null, 
            "name": "Home Warranty", 
            "package_type": "monthly", 
            "phone": "", 
            "purchase_code": null, 
            "rtl": false, 
            "short_name": null, 
            "status": "license_ex", 
            "stripe_id": null, 
            "subscription_plan_id": "613b8a785a2cd24ac1a33bad", 
            "supported_until": null, 
            "trial_ends_at": null, 
            "twilio_account_sid": null, 
            "twilio_application_sid": null, 
            "twilio_auth_token": null, 
            "twilio_enabled": false, 
            "updated_at": "2021-09-15 18:33:32.429033", 
            "website": null
        }
    }
})

function updateCompanies(){
    $(".sidebar-transparent").click();
    companies.companies = [];
    try{
        companyTable.destroy()
    }catch(error){}
    var url = '/api/v1/companies?limit=2000';
    try{
        if(thisCompanyID !== undefined){
            url += '&companyid='+thisCompanyID;
        }
    }catch(error){}
    console.log(url);
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        companies.companies = data;
    }).always(function(){
        setTimeout(function(){
            try{
                companyTable = document.getElementById("company-body");
                console.log(companyTable.nodeName);
                if(companyTable.nodeName == 'TABLE'){
                    companyTable = $('#company-body').DataTable({
                        "order": [[ parseInt(sortColumn), sortStyle ]],
                        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
                        "pageLength": parseInt(pageLength),
                        "language": {
                            "paginate": {
                                "previous": "<<",
                                "next": ">>"
                            }
                        },
                        initComplete: function() {
                            $(this.api().table().container()).find('input[type="search"]').parent().wrap('<form>').parent().attr('autocomplete','off').css('overflow','hidden').css('margin','auto');
                        }   
                    });
                    for(var i = 0; i<hideCols.length; i++){
                        console.log(hideCols[i])
                        companyTable.column(parseInt(hideCols[i])).visible(false);
                        document.getElementById("company-body").style.width = "100%";
                    }
                }
            }catch(error){}
            try{
                document.getElementById('company-body-loading').style.display = 'none';
                document.getElementById('company-body').style.display = '';
            }catch(error){}
        },1000)
    });
}

$('body').on('click','.company-edit', function(){
    var url = '/api/v1/companies?companyid='+$(this).attr('company-id');
    console.log(url);
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        companyDetails.details = data[0];
    });
});

updateCompanies();

$('body').on('click','.login-company', function(){
    var twilio_enabled = $(this).attr('twilio-enabled')=='True'?'twilio':'vicidial';
    window.location = '/set-company-id?companyid='+$(this).attr('company-id')+'&call_type='+twilio_enabled;
});

$('#add-company').click(function(){
    if(validateForm(['#addCompanyName'])){
        var postData = {
            "package_type":"monthly",
            "name":$('#addCompanyName').val(),
            "email":$('#addCompanyEmail').val(),
            "phone":$('#addCompanyPhone').val(),
            "website":$('#addCompanyWebsite').val(),
            "logo":null,
            "address":$('#addCompanyAddress').val(),
            "locale":$('#addCompanyLocale').val(),
            "app_layout":"sidebar",
            "rtl":0,
            "status":$('#addCompanyStatus').val(),
            "licence_expire_on":"2021-09-29",
            "stripe_id":null,
            "card_brand":null,
            "card_last_four":null,
            "trial_ends_at":null,
            "purchase_code":null,
            "supported_until":null,
            "twilio_enabled":true,
            "twilio_account_sid":null,
            "twilio_auth_token":null,
            "twilio_application_sid":null
        }
        try{
            if(!document.getElementById("gen-twilio-account").checked){
                postData['twilio_account_sid'] = $('option:selected', $("#addCompanyTwilio")).attr('twilio_account_sid');
                postData['twilio_auth_token'] = $('option:selected', $("#addCompanyTwilio")).attr('twilio_auth_token');
            }
        }catch(error){
            postData['twilio_account_sid'] = $('option:selected', $("#addCompanyTwilio")).attr('twilio_account_sid');
            postData['twilio_auth_token'] = $('option:selected', $("#addCompanyTwilio")).attr('twilio_auth_token');
        }
        postData['create_twilio_sub'] = document.getElementById("gen-twilio-account").checked;
        console.log(postData);
        postToAPI('/api/v1/companies', postData, 'POST', 'updateCompanies');
    }
})

$('body').on('click','.company-delete', function(){
    companyID = $(this).attr('company-id');
});

$('#company-delete-conf').click(function(){
    var deleteData = {
        'id':companyID
    }
    console.log(deleteData);
    //document.getElementById('company-body-loading').style.display = '';
    //document.getElementById('company-body').style.display = 'none';
    postToAPI('/api/v1/companies', deleteData, 'DELETE', 'updateCompanies');
})

$('body').on('click','#edit-company', function(){
    var updateData = {
        "id":$('#editCompanyID').val(),
        "name":$('#editCompanyName').val(),
        "email":$('#editCompanyEmail').val(),
        "phone":$('#editCompanyPhone').val(),
        "address":$('#editCompanyAddress').val(),
        "locale":$('#editCompanyLocale').val(),
        "app_layout":$('#editCompanyAppLayout').val(),
        "website":$('#editCompanyWebsite').val()
    }
    try{
        updateData['billing'] = {
            'company_id':$('#editCompanyID').val(),
            'charge_type':document.getElementById("charge-minutes").checked?0:1,
            'charge_amount':$("#charge-amount").val()
        }
    }catch(error){}
    console.log(updateData)
    var form_data = new FormData();
    form_data.append('file', $('#companyLogoFile').prop('files')[0]);
    form_data.append('id', $('#editCompanyID').val());
    $.ajax({
        type: 'POST',
        url:  '/api/v1/company-logo',
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        success: function(data) {
            console.log('Success!');
        },
    });
    postToAPI('/api/v1/companies', updateData, 'PUT', 'updateCompanies');
});
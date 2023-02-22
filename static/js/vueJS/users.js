//try{
//    document.getElementById('user-body-loading').style.display = '';
//    document.getElementById('user-body').style.display = 'none';
//}catch(error){}

var usersTable;
try{
    sortColumn = $('#user-body').attr('sort-col');
}catch(error){
    sortColumn = 1
}

try{
    sortStyle = $('#user-body').attr('sort-style');
}catch(error){
    sortStyle = 'asc';
}

try{
    pageLength = $('#user-body').attr('page-length');
}catch(error){
    pageLength = 5;
}

try{
    hideColsRaw = $('#user-body').attr('hide-col');
    hideCols = hideColsRaw.split(',');
}catch(error){
    hideCols = [];
}

var roleCompanies = {};
try{
    document.getElementById("roleHolder").style.display = 'none';
}catch(error){}
var users = new Vue({
    delimiters: ['[[', ']]'],
    el: '#user-body',
    data: {
        users:[],
        roles:[]
    }
})

var userDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#user-edit',
    data: {
        details:{},
        roles:[],
        companies:[],
        roles_full:{}
    }
})

var newUserDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#user-add',
    data: {
        details:{},
        roles:[],
        companies:[]
    }
})

function updateusers(){
    $(".sidebar-transparent").click();
    try{
        usersTable.destroy()
    }catch(error){}
    var url = '/api/v1/users?limit=2000';
    //;
    try{
        url += '&superadmin='+String(superadmin);
    }catch(error){}
    console.log(url);
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        users.users = data['users'];
        console.log(users.users);
        //users.roles = data['roles'];
        //newUserDetails.roles = data['roles'];
        //userDetails.roles = data['roles'];
    }).always(function(){
        setTimeout(function(){
            try{
                usersTable = $('#user-body').DataTable({
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
                    usersTable.column(parseInt(hideCols[i])).visible(false);
                    document.getElementById("user-body").style.width = "100%";
                }
            }catch(error){}
            try{
                document.getElementById('user-body-loading').style.display = 'none';
                document.getElementById('user-body').style.display = '';
            }catch(error){}
        },1000)
    });
    var url = '/api/v1/roles';
    var jqxhr = $.get( url, function(data) {
        newUserDetails.roles = data;
    })
}

$("#user-add-btn").click(function(){
    updateusers();
})

function updateUserCompanies(){
    var url = '/api/v1/companies?limit=2000';
    try{
        url += '&userid='+thisUserID;
    }catch(error){}
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        newUserDetails.companies = data;
        userInviteDetails.companies = data;
    })
}
updateUserCompanies();


function getCurrentUser(){
    var url = '/api/v1/users?limit=2000';
    try{
        url += '&userid='+thisUserID;
    }catch(error){}
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        users.users = data['users'];
    })
}

$('body').on('click','.company-role', function(){
    var companyRoleClasses = document.getElementsByClassName('company-role');
    roleCompanies = {};
    console.log(newUserDetails.roles);
    for(var x = 0; x<companyRoleClasses.length; x++){
        var companyID = $(companyRoleClasses[x]).attr('name');
        if(companyRoleClasses[x].checked){
            //console.log(companyID);
            for(var i = 0; i<newUserDetails.roles.length; i++){
                if(String(newUserDetails.roles[i]['company_id']) == companyID){
                    companyName = newUserDetails.roles[i]['company_name']
                    try{
                        roleCompanies[companyName].push(newUserDetails.roles[i]);
                    }catch(error){
                        roleCompanies[companyName] = [];
                        roleCompanies[companyName].push(newUserDetails.roles[i]);
                    }
                }
            }
        }
    }
    console.log(roleCompanies);
    var roleCompanyHTML = '';
    document.getElementById("company-roles").innerHTML = '';
    var companies = Object.keys(roleCompanies);
    for(var i = 0; i<companies.length; i++){
        roleCompanyHTML += '<div class="mt-4">';
        roleCompanyHTML += '<h2>'+companies[i]+'</h2>';
        roleCompanyHTML += '<select class = "addUserRoles form-control">';
        for(var j = 0; j<roleCompanies[companies[i]].length; j++){
            var roleDetails = roleCompanies[companies[i]][j];
            roleCompanyHTML += '<option value="'+roleDetails['id']+'"> '+roleDetails['name']+'</option>';
        }
        roleCompanyHTML += '</select>';
        roleCompanyHTML += '</div>';
    }
    document.getElementById("company-roles").innerHTML = roleCompanyHTML;
    document.getElementById("roleHolder").style.display = '';
    console.log(roleCompanyHTML);
    if(roleCompanyHTML == ''){
        document.getElementById("roleHolder").style.display = 'none';
    }
})

$('body').on('click','.user-edit', function(){
    var finishedUsers = false;
    var finishedRoles = false;
    var fullData = {}
    $("#reset-password-user").prop( "disabled", true );
    var url = '/api/v1/users?userid='+$(this).attr('user-id');
    try{
        document.getElementById("user-edit-loading").style.display = "";
        document.getElementById("user-edit-body").style.display = "none";
    }catch(error){}
    var jqxhr = $.get( url, function(data) {
        userDetails.details = data['users'][0];
        fullData['users'] = data['users'][0];
        $("#reset-password-user").prop( "disabled", false );
    })
    .always(function() {
        console.log(fullData);
        finishedUsers = true;
        if(finishedUsers && finishedRoles){
            console.log(finishedUsers);
            console.log(finishedRoles);
            try{
                document.getElementById("user-edit-loading").style.display = "none";
                document.getElementById("user-edit-body").style.display = "";
            }catch(error){}
            updateEditRoles(fullData);
        }
    });

    var url = '/api/v1/roles';
    try{
        document.getElementById("user-edit-loading").style.display = "";
        document.getElementById("user-edit-body").style.display = "none";
    }catch(error){}
    var jqxhr = $.get( url, function(data) {
        userDetails.roles = data;
        fullData['roles'] = data;
    })
    .always(function() {
        console.log(fullData);
        finishedRoles = true;
        if(finishedUsers && finishedRoles){
            console.log(finishedUsers);
            console.log(finishedRoles);
            try{
                document.getElementById("user-edit-loading").style.display = "none";
                document.getElementById("user-edit-body").style.display = "";
            }catch(error){}
            updateEditRoles(fullData);
        }
    });
});

function updateEditRoles(data){
    userDetails.companies = [];
    userDetails.roles_full = {};
    var companies = [];
    var roles = {};
    //try{
        for(var i = 0; i<data['roles'].length; i++){
            role_dict = {
                'id':data['roles'][i]['id'],
                'name':data['roles'][i]['display_name'],
                'company_name':data['roles'][i]['company_name'],
                'enabled':false
            }
            company_dict = {
                'company_id':data['roles'][i]['company_id'],
                'name':data['roles'][i]['company_name'],
                'enabled':false
            }
            for(var j = 0; j<data['users']['roles'].length; j++){
                if(company_dict['company_id'] == data['users']['roles'][j]['company_id']){
                    company_dict['enabled'] = true;
                    role_dict['enabled'] = true;
                }
            }
                
            if(!companies.includes(company_dict)){
                companies.push(company_dict);
            }
            try{
                roles[company_dict['company_id']].push(role_dict);
            }catch(error){
                roles[company_dict['company_id']] = [];
                roles[company_dict['company_id']].push(role_dict);
            }
        }
        console.log(roles);
        userDetails.companies = companies;
        userDetails.roles_full = roles;
        setTimeout(function(){
            var toggles = document.getElementsByClassName("company-role-edit");
            for(var i = 0; i<toggles.length; i++){
                console.log("Sending Clicks");
                toggles[i].click();
            }
        },1000)
        setTimeout(function(){
            var toggles = document.getElementsByClassName("company-role-edit");
            for(var i = 0; i<toggles.length; i++){
                console.log("Sending Clicks");
                toggles[i].click();
            }
        },1000)
    //}catch(error){}
}


$('body').on('click','.company-role-edit', function(){
    var index = parseInt($(this).attr('index'));
    userDetails.companies[index]['enabled'] = this.checked;
});

updateusers();

$('body').on('click','#add-user', function(){
    if(validateForm(['#addUserEmail'])){
        var postData = {
            "first_name":$('#addUserFName').val(),
            "last_name":$("#addUserLName").val(),
            "skype_id":$("#addUserSkype").val(),
            "email":$("#addUserEmail").val(),
            "address":$("#addUserAddress").val(),
            "country":$("#addUserCountry").val(),
            "zip_code":$("#addUserZip").val(),
            "password":$("#addUserPassword").val(),
            "contact_number":$("#addUserContact").val()
        }
        try{
            postData['super_admin'] = superadmin==1?true:false;
        }catch(error){}
        var roleClasses = document.getElementsByClassName("addUserRoles");
        var roles = [];
        for(var i = 0; i<roleClasses.length; i++){
            console.log($(roleClasses[i]).val());
            roles.push({
                'role_id':$(roleClasses[i]).val()
            })
        }
        if(roles.length > 0){
            postData['roles'] = roles;
        
            console.log(postData);
            postToAPI('/api/v1/users', postData, 'POST', 'updateusers');
        }
    }
});


var userInviteDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#user-activate',
    data: {
        smtp_companies:[],
        companies:[],
        user_id:null
    }
})

$('body').on('click','.user-invite', function(){
    var url = '/api/v1/users?userid='+$(this).attr('user-id');

    document.getElementById("user-invite-loading").style.display = '';
    document.getElementById("user-invite-select").style.display = 'none';
    $("#user-send").prop( "disabled", true );

    var jqxhr = $.get( url, function(data) {
        var temp_roles =  data['users'][0]['roles'];
        userInviteDetails.user_id = data['users'][0]['id'];
        for(var i = 0; i<temp_roles.length; i++){
            for(var j = 0; j<userInviteDetails.companies.length; j++){
                if(temp_roles[i]['company_id'] == userInviteDetails.companies[j]['id']){
                    temp_roles[i]['company_name'] = userInviteDetails.companies[j]['name']
                }
            }
        }
        userInviteDetails.smtp_companies = temp_roles;

        document.getElementById("user-invite-loading").style.display = 'none';
        document.getElementById("user-invite-select").style.display = '';

        $("#user-send").prop( "disabled", false );
    });
})

$('body').on('click','#user-send', function(){
    var post_data = {
        "company_id":$("#user-invite-select").val(),
        "user_id":userInviteDetails.user_id
    }
    console.log(post_data);
    postToAPI('/api/v1/users/signup', post_data, 'POST', 'updateusers');
});

$('body').on('click','#edit-user', function(){
    //if(validateForm(['#editUserID', '#editUserFName'])){
        var updateData = {}
        updateData['id'] = $('#editUserID').val();
        try{if($('#editUserFName').val() !== undefined){updateData['first_name'] = $('#editUserFName').val()}}catch(error){}
        try{if($('#editUserLName').val() !== undefined){updateData['last_name'] = $('#editUserLName').val()}}catch(error){}
        try{if($('#editUserSkypeID').val() !== undefined){updateData['skype_id'] = $('#editUserSkypeID').val()}}catch(error){}
        try{
            if($('#editUserEmail').val() !== undefined){
                var user_email_split = String($('#editUserEmail').val()).split(' ')
                var user_email = user_email_split.join()
                updateData['email'] = user_email;
            }
        }catch(error){}
        try{if($('#editUserAddress').val() !== undefined){updateData['address'] = $('#editUserAddress').val()}}catch(error){}
        try{if($('#editUserCountry').val() !== undefined){updateData['country'] = $('#editUserCountry').val()}}catch(error){}
        try{if($('#editUserZip').val() !== undefined){updateData['zip_code'] = $('#editUserZip').val()}}catch(error){}
        try{if($('#editUserTimeZone').val() !== undefined){updateData['timezone'] = $('#editUserTimeZone').val()}}catch(error){}
        try{if($('#editUserDateFormat').val() !== undefined){updateData['date_format'] = $('#editUserDateFormat').val()}}catch(error){}
        try{if($('#editUserTimeFormat').val() !== undefined){updateData['time_format'] = $('#editUserTimeFormat').val()}}catch(error){}
        try{if($('#editUserContact').val() !== undefined){updateData['contact_number'] = $('#editUserContact').val()}}catch(error){}
        console.log($('#editUserPassword').val());
        if($('#editUserPassword').val() != ''){
            var password = $('#editUserPassword').val();
            if(password.length >= 8){
                var includesLowerCase = false;
                var includesUpperCase = false;
                var includesNumber = false;
                var includesSpecial = false;

                var lowerCase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];
                var upperCase = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
                var numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'];
                var specials = ['!', '?', '<', '>', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+'];

                var passwordSplit = password.split('');
                for(var i = 0; i<passwordSplit.length; i++){
                    if(lowerCase.includes(passwordSplit[i])){
                        includesLowerCase = true;
                    }
                    if(upperCase.includes(passwordSplit[i])){
                        includesUpperCase = true;
                    }
                    if(numbers.includes(passwordSplit[i])){
                        includesNumber = true;
                    }
                    if(specials.includes(passwordSplit[i])){
                        includesSpecial = true;
                    }
                }
                var check = 0;
                if(includesLowerCase){
                    check++;
                }
                if(includesUpperCase){
                    check++;
                }
                if(includesNumber){
                    check++;
                }
                if(includesSpecial){
                    check++;
                }
                if(check >= 3){
                    $('#editUserPassword').removeClass('border'); 
                    $('#editUserPassword').removeClass('border-danger'); 
                    var warningID = 'editUserPassword-warning';
                    try{
                        document.getElementById(warningID).remove();
                    }catch(error){}
                    updateData['password'] = password;
                }
                else{
                    $('#editUserPassword').addClass('border'); 
                    $('#editUserPassword').addClass('border-danger'); 
                    var warningID = 'editUserPassword-warning';
                    var html = '<span id="'+warningID+'" class="text-danger">Password does not meet requirements</span>';
                    $('#editUserPassword').parent().append(html);
                }
            }
            else{
                $('#editUserPassword').addClass('border'); 
                $('#editUserPassword').addClass('border-danger'); 
                var warningID = 'editUserPassword-warning';
                var html = '<span id="'+warningID+'" class="text-danger">Password does not meet requirements</span>';
                $('#editUserPassword').parent().append(html);
            }
        }
        var roleClasses = document.getElementsByClassName("editUserRoles");
        var roles = [];
        for(var i = 0; i<roleClasses.length; i++){
            console.log($(roleClasses[i]).attr('name'));
            roles.push({
                'role_id':$(roleClasses[i]).attr('name'),
                'enabled':roleClasses[i].checked
            })
        }
        if(roles.length > 0){
            updateData['roles'] = roles;
            updateData['clear_roles'] = false;
        }
        else{
            var roleClasses = document.getElementsByClassName("editUserRoles-new");
            for(var i = 0; i<roleClasses.length; i++){
                console.log($(roleClasses[i]).val());
                roles.push({
                    'role_id':$(roleClasses[i]).val()
                })
            }
            if(roles.length > 0){
                updateData['roles'] = roles;
                updateData['clear_roles'] = true;
            }
        }
        console.log(updateData);
        try{
            var form_data = new FormData();
            form_data.append('file', $('#editUsrImgFile').prop('files')[0]);
            form_data.append('id', $('#editUserID').val());
            $.ajax({
                type: 'POST',
                url:  '/api/v1/user-img',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                success: function(data) {
                    console.log('Success!');
                },
            });
            console.log(form_data);
        }catch(error){}
        postToAPI('/api/v1/users', updateData, 'PUT', 'updateusers');
    //}
});

var userID;
$('body').on('click','.user-delete', function(){
    userID = $(this).attr('user-id');
});

$('#user-delete-conf').click(function(){
    var deleteData = {
        'id':userID
    }
    console.log(deleteData);
    //document.getElementById('company-body-loading').style.display = '';
    //document.getElementById('company-body').style.display = 'none';
    postToAPI('/api/v1/users', deleteData, 'DELETE', 'reloadPage');
})
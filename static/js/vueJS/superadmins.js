var roleCompanies = {};
try{
    document.getElementById("roleHolder").style.display = 'none';
}catch(error){}
var superAdmins = new Vue({
    delimiters: ['[[', ']]'],
    el: '#admin-table',
    data: {
        users:[],
        roles:[]
    }
})

var superAdminDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#admin-edit',
    data: {
        details:{},
        roles:[],
        companies:[]
    }
})

var newSuperAdminDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#admin-new',
    data: {
        details:{},
        roles:[],
        companies:[]
    }
})

function updateSuperAdmins(){
    $(".sidebar-transparent").click();
    var url = '/api/v1/users?superadmin=1&limit=2000';
    try{
        url += '&userid='+thisUserID;
    }catch(error){}
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        superAdmins.users = data['superAdmins'];
        superAdmins.roles = data['roles'];
        newSuperAdminDetails.roles = data['roles'];
        superAdminDetails.roles = data['roles'];
    })
}

function updateUserCompanies(){
    var url = '/api/v1/companies?limit=2000';
    try{
        url += '&userid='+thisUserID;
    }catch(error){}
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        newSuperAdminDetails.companies = data;
    })
}
updateUserCompanies();

$('body').on('click','.company-role', function(){
    var companyRoleClasses = document.getElementsByClassName('company-role');
    roleCompanies = {};
    for(var x = 0; x<companyRoleClasses.length; x++){
        var companyID = $(companyRoleClasses[x]).attr('name');
        if(companyRoleClasses[x].checked){
            for(var i = 0; i<newSuperAdminDetails.roles.length; i++){
                if(String(newSuperAdminDetails.roles[i]['company_id']) == companyID){
                    companyName = newSuperAdminDetails.roles[i]['company_name']
                    try{
                        roleCompanies[companyName].push(newSuperAdminDetails.roles[i]);
                    }catch(error){
                        roleCompanies[companyName] = [];
                        roleCompanies[companyName].push(newSuperAdminDetails.roles[i]);
                    }
                }
            }
        }
    }
    var roleCompanyHTML = '';
    document.getElementById("company-roles").innerHTML = '';
    var companies = Object.keys(roleCompanies);
    for(var i = 0; i<companies.length; i++){
        roleCompanyHTML += '<div class="mt-4">';
        roleCompanyHTML += '<h2>'+companies[i]+'</h2>';
        for(var j = 0; j<roleCompanies[companies[i]].length; j++){
            var roleDetails = roleCompanies[companies[i]][j];
            roleCompanyHTML += '<div>';
            roleCompanyHTML += '<input class="default-forms addUserRoles" type="checkbox" name="'+roleDetails['id']+'">';
            roleCompanyHTML += '<label for="'+roleDetails['id']+'" class="ml-1"> '+roleDetails['name']+'</label>';
            roleCompanyHTML += '</div>';
        }
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
    var url = '/api/v1/users?userid='+$(this).attr('user-id');
    var jqxhr = $.get( url, function(data) {
        superAdminDetails.details = data['superAdmins'][0];
        superAdminDetails.roles = data['roles'];
    });
});

updateSuperAdmins();

$('body').on('click','#add-user', function(){
    var postData = {
        "first_name":$('#addUserFName').val(),
        "last_name":$("#addUserLName").val(),
        "skype_id":$("#addsuperAdminskype").val(),
        "email":$("#addUserEmail").val(),
        "address":$("#addUserAddress").val(),
        "country":$("#addUserCountry").val(),
        "zip_code":$("#addUserZip").val(),
        "password":$("#addUserPassword").val(),
        "contact_number":$("#addUserContact").val()
    }
    var roleClasses = document.getElementsByClassName("addUserRoles");
    var roles = [];
    for(var i = 0; i<roleClasses.length; i++){
        console.log($(roleClasses[i]).attr('name'));
        if(roleClasses[i].checked){
            roles.push({
                'role_id':$(roleClasses[i]).attr('name')
            })
        }
    }
    if(roles.length > 0){
        postData['roles'] = roles;
    }
    
    console.log(postData);
    postToAPI('/api/v1/users', postData, 'POST', 'updateSuperAdmins');
});

$('body').on('click','#edit-user', function(){
    //if(validateForm(['#editUserID', '#editUserFName'])){
        var updateData = {}
        updateData['id'] = $('#editUserID').val();
        try{if($('#editUserFName').val() !== undefined){updateData['first_name'] = $('#editUserFName').val()}}catch(error){}
        try{if($('#editUserLName').val() !== undefined){updateData['last_name'] = $('#editUserLName').val()}}catch(error){}
        try{if($('#editsuperAdminskypeID').val() !== undefined){updateData['skype_id'] = $('#editsuperAdminskypeID').val()}}catch(error){}
        try{if($('#editUserEmail').val() !== undefined){updateData['email'] = $('#editUserEmail').val()}}catch(error){}
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
        }
    
        console.log(updateData);
        postToAPI('/api/v1/users', updateData, 'PUT', 'updateSuperAdmins');
    //}
});
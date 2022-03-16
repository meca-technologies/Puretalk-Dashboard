try{
    document.getElementById('role-body-loading').style.display = '';
    document.getElementById('role-body').style.display = 'none';
}catch(error){}
var roleID;

var roles = new Vue({
    delimiters: ['[[', ']]'],
    el: '#role-body',
    data: {
        roles:[]
    }
});

var roleDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#role-edit',
    data: {
        details:{},
        companies:[]
    }
});

function updateRoles(){
    $(".sidebar-transparent").click();
    var jqxhr = $.get( '/api/v1/roles', function(data) {
        console.log(data);
        roles.roles = data;
        try{
            $("#role-body-loading").fadeOut();
            $("#role-body-loading").promise().done(function(){
                $("#role-body").fadeIn();
            });
        }catch(error){}
    })
}

$('body').on('click','.role-edit', function(){
    var url = '/api/v1/roles-details?roleid='+$(this).attr('role-id');
    console.log(url);
    roleDetails.details = {
        'name':"role_name"
    }
    try{
        document.getElementById('role-details-body-loading').style.display = '';
        document.getElementById('role-details-body').style.display = 'none';
    }catch(error){}
    var jqxhr = $.get( url, function(data) {
        roleDetails.details = data[0];
        try{
            document.getElementById('role-details-body-loading').style.display = 'none';
            document.getElementById('role-details-body').style.display = '';
        }catch(error){}
    });

    var jqxhr = $.get( '/api/v1/companies', function(data) {
        console.log(data);
        roleDetails.companies = data;
    });
});

updateRoles();

$('body').on('click','#edit-role', function(){
    try{
        document.getElementById('role-details-body-loading').style.display = '';
        document.getElementById('role-details-body').style.display = 'none';
    }catch(error){}
    roleID = $("#edit-role-id").val();
    var updateData = {
        "id":roleID,
        "company_id":$("#edit-role-company").val(),
        "name":$("#edit-role-name").val(),
        "display_name":$("#edit-role-display").val(),
        "description":$("#edit-role-descr").val()
    }
    var permissions = document.getElementsByClassName("permission-check");
    permissionData = [];
    for(var i = 0; i<permissions.length; i++){
        permissionData.push({
            "id":$(permissions[i]).attr("permssion-id"),
            "name":$(permissions[i]).attr("name"),
            "display_name":$(permissions[i]).attr("display-name"),
            "enabled":permissions[i].checked?true:false,
            "role_id":roleID
        })
    }
    updateData['permissions'] = permissionData;
    console.log(updateData);
    postToAPI('/api/v1/roles', updateData, 'PUT', 'updateRoles');
});

$('body').on('click','#add-role', function(){
    var postData = {
        "company_id":$("#company-body").val(),
        "name":$("#add-role-name").val(),
        "display_name":$("#add-role-display").val(),
        "description":$("#add-role-descr").val()
    }
    console.log(postData);
    postToAPI('/api/v1/roles', postData, 'POST', 'updateRoles');
});

$('body').on('click','.role-delete', function(){
    roleID = $(this).attr("role-id");
})

$('body').on('click','#role-delete-conf', function(){
    var deleteData = {
        "id":roleID
    }
    console.log(deleteData);
    postToAPI('/api/v1/roles', deleteData, 'DELETE', 'updateRoles');
});

$("#selectAllPerms").click(function(){
    var permissions = document.getElementsByClassName("permission-check");
    for(var i = 0; i<permissions.length; i++){
        permissions[i].checked = true;
    }
})

$("#deselectAllPerms").click(function(){
    var permissions = document.getElementsByClassName("permission-check");
    for(var i = 0; i<permissions.length; i++){
        permissions[i].checked = false;
    }
})
var virtualAgentsAdmin = new Vue({
    delimiters: ['[[', ']]'],
    el: '#virtual-agent-admin-body',
    data: {
        virtualAgentsAdmin:[],
        showInactive:false
    }
})
var virtualAgentDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#virtual-agent-edit',
    data: {
        details:{},
        companies:[]
    }
})

function updateVirtualAgentsAdmin(){
    $(".sidebar-transparent").click();
    var jqxhr = $.get( '/api/v1/virtual-agents?limit=2000', function(data) {
        console.log(data);
        virtualAgentsAdmin.virtualAgentsAdmin = data;
    })
    var url = '/api/v1/companies?limit=2000';
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        virtualAgentDetails.companies = data;
    });
}

updateVirtualAgentsAdmin();

$("#virtual-show-inactive").click(function(){
    var show = $(this).attr("show");
    if(show == "false"){
        this.innerHTML = 'Hide Inactive';
        virtualAgentsAdmin.showInactive = true;
        $(this).attr("show","true");
    }
    else{
        this.innerHTML = 'Show Inactive';
        virtualAgentsAdmin.showInactive = false;
        $(this).attr("show","false");
    }
})

$('#add-virtual-agent').click(function(){
    var postData = {
        "company_id":$('#company-body').val(),
        "name":$('#add-agent-name').val(),
        "studio_name":$('#add-agent-studio').val(),
        "phone":$('#add-agent-phone').val(),
        "xfer":$('#add-agent-xfer').val(),
        "voice_url":$('#add-agent-voice').val(),
        "app_id":$('#add-agent-app').val(),
        "status":document.getElementById('add-agent-enabled').checked == true?true:false
    }
    console.log(postData);
    postToAPI('/api/v1/virtual-agents', postData, 'POST', 'updateVirtualAgentsAdmin');
});

$('body').on('click','.virtual-agent-edit', function(){
    var url = '/api/v1/virtual-agents?agentid='+$(this).attr('agent-id');
    var jqxhr = $.get( url, function(data) {
        console.log(data[0]);
        virtualAgentDetails.details = data[0];
    });
    var url = '/api/v1/companies?limit=2000';
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        virtualAgentDetails.companies = data;
    });
});

$('#edit-virtual-agent').click(function(){
    var updateData = {
        "id":$('#edit-agent-id').val(),
        "company_id":$('#edit-company-body').val(),
        "name":$('#edit-agent-name').val(),
        "studio_name":$('#edit-agent-studio').val(),
        "phone":$('#edit-agent-phone').val(),
        "xfer":$('#edit-agent-xfer').val(),
        "app_id":$('#edit-agent-app').val(),
        "voice_url":$('#edit-agent-voice').val(),
        "status":document.getElementById('edit-agent-enabled').checked == true?true:false
    }
    console.log(updateData);
    postToAPI('/api/v1/virtual-agents', updateData, 'PUT', 'updateVirtualAgentsAdmin');
});

var deleteID;
$('body').on('click','.virtual-agent-delete', function(){
    deleteID = $(this).attr('agent-id');
});

$("#agent-delete-conf").click(function(){
    var deleteData = {
        "id":deleteID
    }
    console.log(deleteData);
    postToAPI('/api/v1/virtual-agents', deleteData, 'DELETE', 'updateVirtualAgentsAdmin');
})
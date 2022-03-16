var group_id;
var outbound_cid;

try{
    document.getElementById('caller-id-group-loading').style.display = '';
    document.getElementById('caller-id-group-body').style.display = 'none';
}catch(error){}

var caller_id_groups = new Vue({
    delimiters: ['[[', ']]'],
    el: '#caller-id-group-body',
    data: {
        caller_id_groups:[]
    }
})

var caller_ids = new Vue({
    delimiters: ['[[', ']]'],
    el: '#caller-id-table',
    data: {
        caller_ids:[]
    }
})

function getCallerIDGroups(){
    try{
        $("#caller-id-group-loading").fadeIn();
        $("#caller-id-group-loading").promise().done(function(){
            $("#caller-id-group-body").fadeOut();
        });
    }catch(error){}
    var jqxhr = $.get( '/api/vici/caller_id_groups', function(data) {
        console.log(data);
        caller_id_groups.caller_id_groups = data['data'];
        try{
            $("#caller-id-group-loading").fadeOut();
            $("#caller-id-group-loading").promise().done(function(){
                $("#caller-id-group-body").fadeIn();
            });
        }catch(error){}
    })
}

getCallerIDGroups();

$('body').on('change','#caller-id-group-body', function(){
    console.log($(this).val());
    if($(this).val() != ''){
        try{
            $("#caller-id-table").fadeOut();
            $("#caller-id-table").promise().done(function(){
                $("#caller-id-table-loading").fadeIn();
            });
        }catch(error){}
        var url = '/api/vici/caller_ids?group_id='+$(this).val();
        var jqxhr = $.get( url, function(data) {
            console.log(data);
            caller_ids.caller_ids = data['data'];
            try{
                $("#caller-id-table-loading").fadeOut();
                $("#caller-id-table-loading").promise().done(function(){
                    $("#caller-id-table").fadeIn();
                });
            }catch(error){}
        })
    }
})

$('body').on('click','.cid_active', function(){
    try{
        $("#caller-id-table").fadeOut();
        $("#caller-id-table").promise().done(function(){
            $("#caller-id-table-loading").fadeIn();
        });
    }catch(error){}
    var post_data = {
        "group_id":$(this).attr('group-id'),
        "outbound_cid":$(this).attr('outbound-cid'),
        "active":$(this).attr('active-set')
    }
    console.log(post_data);
    postToAPI('/api/vici/caller_ids', post_data, 'PUT', 'getCallerIDGroups');
})

$('body').on('click','#caller-id-add', function(){
    group_id = $(this).attr('group-id');
});

$("#caller-id-add-conf").click(function(){
    try{
        document.getElementById('caller-id-table-loading').style.display = '';
        document.getElementById('caller-id-table').style.display = 'none';
    }catch(error){}
    var post_data = {
        'group_id':group_id,
        'areacode': $("#addCallerIDArea").val(),
        'outbound_cid': $("#addCallerIDCID").val(),
        'cid_description': $("#addCallerIDDescr").val()
    }
    console.log(post_data);
    postToAPI('/api/vici/caller_ids', post_data, 'POST', 'getCallerIDGroups');
})

$('body').on('click','.caller-id-delete', function(){
    group_id = $(this).attr('group-id');
    outbound_cid = $(this).attr('outbound-cid');
});

$("#caller-id-delete-conf").click(function(){
    try{
        document.getElementById('caller-id-table-loading').style.display = '';
        document.getElementById('caller-id-table').style.display = 'none';
    }catch(error){}
    var delete_data = {
        'group_id':group_id,
        'outbound_cid': outbound_cid
    }
    console.log(delete_data);
    postToAPI('/api/vici/caller_ids', delete_data, 'DELETE', 'getCallerIDGroups');
})
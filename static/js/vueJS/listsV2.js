try{
    document.getElementById('list-body-loading').style.display = '';
    document.getElementById('list-body').style.display = 'none';
}catch(error){}

var list_id;

var lists = new Vue({
    delimiters: ['[[', ']]'],
    el: '#list-body',
    data: {
        lists:[]
    }
})

var listDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#list-edit',
    data: {
        details:{},
        campaigns:[]
    }
})

function updateLists(){
    $(".sidebar-transparent").click();
    try{
        $("#list-body-loading").fadeIn();
        $("#list-body-loading").promise().done(function(){
            $("#list-body").fadeOut();
        });
    }catch(error){}
    var jqxhr = $.get( '/api/vici/lists', function(data) {
        console.log(data);
        lists.lists = data['data'];
        try{
            $("#list-body-loading").fadeOut();
            $("#list-body-loading").promise().done(function(){
                $("#list-body").fadeIn();
            });
        }catch(error){}
    });
    
    var jqxhr = $.get( '/api/vici/campaigns', function(data) {
        console.log(data);
        listDetails.campaigns = data['data'];
    })
}

updateLists();

$("#add-list").click(function(){
    var post_data = {
        "list_id":$("#addListID").val(),
        "list_name":$("#addListName").val(),
        "list_description":$("#addListDescription").val(),
        "campaign_id":$("#campaign-body").val(),
        "active":$("#addListActive").val()
    }
    console.log(post_data);
    postToAPI('/api/vici/lists', post_data, 'POST', 'updateLists');
})

$('body').on('click','.list-edit', function(){
    list_index = $(this).attr('list-id');
    listDetails.details = lists.lists[list_index];
    list_id = listDetails.details['list_id'];
    console.log(list_id);
    try{
        document.getElementById('list-edit-loading').style.display = 'none';
        document.getElementById('list-edit-body').style.display = '';
    }catch(error){}
});

$("#edit-list").click(function(){
    var post_data = {
        "list_id":list_id,
        "list_name":$("#editListName").val(),
        "list_description":$("#editListDescription").val(),
        "campaign_id":$("#edit-campaign-body").val(),
        "active":$("#editListActive").val()
    }
    console.log(post_data);
    postToAPI('/api/vici/lists', post_data, 'PUT', 'updateLists');
});

$('body').on('click','.list-delete', function(){
    list_id = $(this).attr('list-id');
});

$("#list-delete-conf").click(function(){
    var delete_data = {
        "list_id":list_id
    }
    console.log(delete_data);
    postToAPI('/api/vici/lists', delete_data, 'DELETE', 'updateLists');
})
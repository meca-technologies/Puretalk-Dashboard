const urlSearchParams = new URLSearchParams(window.location.search);
const params = Object.fromEntries(urlSearchParams.entries());
try{
    document.getElementById('campaign-edit-loading').style.display = '';
    document.getElementById('campaign-edit-body').style.display = 'none';
}catch(error){}

var campaignID;

var campaigns = new Vue({
    delimiters: ['[[', ']]'],
    el: '#campaign-body',
    data: {
        campaigns:[]
    }
})

var campaignDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#campaign-edit',
    data: {
        details:{},
        lists:[],
        caller_id_groups:[]
    }
})

function updateCampaigns(){
    $(".sidebar-transparent").click();
    try{
        $("#campaign-body").fadeOut();
        $("#campaign-body").promise().done(function(){
            $("#campaign-body-loading").fadeIn();
        });
    }catch(error){}
    var jqxhr = $.get( '/api/vici/campaigns', function(data) {
        console.log(data);
        campaigns.campaigns = data['data'];
    }).always(function(){
        try{
            $("#campaign-body-loading").fadeOut();
            $("#campaign-body-loading").promise().done(function(){
                $("#campaign-body").fadeIn();
            });
        }catch(error){}
        setTimeout(function(){
            try{
                console.log(params['campaign_id']);
                if(params['campaign_id'] !== undefined && params['campaign_id'] != ''){
                    document.getElementById("campaign-body").value = params['campaign_id'];
                    try{
                        $("#lead-filter-report").click();
                    }catch(error){}
                }
            }catch(error){}
        },500);
        setTimeout(function(){
            calculateProgressBars();
            updateNotification();
            try{
                $("#lead-filter-report").click();
            }catch(error){}
        },1000);
    });
    
    var jqxhr = $.get( '/api/vici/caller_id_groups', function(data) {
        console.log(data);
        campaignDetails.caller_id_groups = data['data'];
    })
}
updateCampaigns();

$('#add-company').click(function(){
    postData = {
        "park_ext":"",
        "campaign_id":$("#addCampaignID").val(),
        "campaign_name":$("#addCampaignName").val(),
        "campaign_description":$("#addCampaignDescription").val(),
        "user_group":"---ALL---",
        "active":$("#addCampaignActive").val(),
        "park_file_name":"",
        "web_form_address":"",
        "allow_closers":"Y",
        "hopper_level":$("#addCampaignHopperLevel").val(),
        "number_of_lines":$("#addCampaignNumLines").val(),
        "auto_dial_level":"3",
        "next_agent_call":"random",
        "local_call_time":"9am-5pm",
        "voicemail_ext":"",
        "script_id":"",
        "campaign_script_two":"",
        "get_call_launch":"NONE",
        "SUBMIT":"SUBMIT"
    }
    postToAPI('/api/vici/campaigns', postData, 'POST', 'updateCampaigns');
});

$('body').on('click','#edit-company', function(){
    try{
        document.getElementById('campaign-edit-loading').style.display = '';
        document.getElementById('campaign-edit-body').style.display = 'none';
    }catch(error){}
    
    var postData = {
        'campaign_id':campaignID,
        'campaign_name':$('#campaignEditName').val(),
        'dial_timeout':$('#campaignEditDialTimeout').val(),
        'campaign_cid':$('#campaignCallerID').val(),
        'hopper_level':$('#campaignEditHopperLevel').val(),
        'campaign_cid':$('#campaignEditCID').val(),
        'cid_group_id':$('#campaignEditCallerIDGroup').val(),
        'number_of_lines':$('#campaignEditNumLines').val(),
        'xferconf_a_dtmf':$('#campaignEditDID').val(),
        'active':$('#campaignEditActive').val()
    }
    postToAPI('/api/vici/campaigns', postData, 'PUT', 'updateCampaigns');
});

$('body').on('click','.campaign-edit', function(){
    campaign_index = $(this).attr('campaign-id');
    console.log(campaign_index);
    campaignDetails.details = campaigns.campaigns[campaign_index];
    console.log(campaignDetails.details);
    campaignID = campaigns.campaigns[campaign_index]['campaign_id'];
    campaignDetails.lists = campaigns.campaigns[campaign_index]['extra_detail']['lists'];
    console.log(campaignDetails.lists);
    console.log(campaignDetails);
    try{
        document.getElementById('campaign-edit-loading').style.display = 'none';
        document.getElementById('campaign-edit-body').style.display = '';
    }catch(error){}
    setTimeout(function(){
        var length = String(document.getElementById("campaignEditCID").value).length;

        for(var i = length; i<10; i++){
            document.getElementById("campaignEditCID").value += '0';
        }
    },100);
});

$('body').on('click','.campaign-delete', function(){
    campaign_index = $(this).attr('campaign-id');
    campaignID = campaigns.campaigns[campaign_index]['campaign_id'];
});

$('#campaign-delete-conf').click(function(){
    var deleteData = {
        'campaign_id':campaignID
    }
    console.log(deleteData);
    postToAPI('/api/vici/campaigns', deleteData, 'DELETE', 'updateCampaigns');
});

function getLeadDifference(total, called){
    return call-(total-called);
}

$('body').on('click','.lead-export', function(){
    var url = '/api/vici/leads/export?campaign_id='+$(this).attr('campaign-id');
    var csv = '';
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        data.forEach(function(row) {
            csv += row.join(',');
            csv += "\n";
        });
        console.log(csv);
        var hiddenElement = document.createElement('a');
        hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
        hiddenElement.target = '_blank';
        hiddenElement.download = 'leads.csv';
        hiddenElement.click();
    })
});
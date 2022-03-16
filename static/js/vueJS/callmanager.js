try{
    document.getElementById('call-manager-body-loading').style.display = '';
    document.getElementById('call-manager-body').style.display = 'none';
}catch(error){}
calculateProgressBars();

var callCampaigns = new Vue({
    delimiters: ['[[', ']]'],
    el: '#call-manager-body',
    data: {
        campaigns:[],
        showComplete:true
    }
})

function updateCallCampaigns(){
    console.log('Update Call Campaigns');
    callCampaigns.campaigns = [];
    try{
        document.getElementById('call-manager-body-loading').style.display = '';
        document.getElementById('call-manager-body').style.display = 'none';
    }catch(error){}
    var jqxhr = $.get( '/api/v1/campaigns?limit=2000&summary=1', function(data) {
        console.log(data);
        callCampaigns.campaigns = data;
    }).always(function(){
        try{
            document.getElementById('call-manager-body-loading').style.display = 'none';
            document.getElementById('call-manager-body').style.display = '';
        }catch(error){}
        setTimeout(function(){
            calculateProgressBars();
        },1000);
    });
}

$('body').on('click','.control-campaign', function(){
    var updateData = {
        'status':$(this).attr('campaign-status'),
        'id':$(this).attr('campaign-id')
    }
    console.log(updateData);
    postToAPI('/api/v1/campaigns', updateData, 'PUT', 'updateCallCampaigns');
});

var leadFormDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#lead-form-details',
    data: {
        details:[],
        caller_ids:[]
    }
})

var campaignID;
$('body').on('click','.campaign-call', function(){
    campaignID = $(this).attr('campaign-id');
    
    csvDetails.fields = [];
    csvDetails.fullDetails = [];
    document.getElementById("lead-form-details-loading").style.display = '';
    document.getElementById("lead-form-details").style.display = 'none';
    var jqxhr = $.get( '/api/v1/campaigns?campaignid='+campaignID, function(data) {
        var newFormID = data[0]['form_id'];
        var url = '/api/v1/forms?formid='+newFormID;
        leadFormDetails.caller_ids = data[0]['caller_ids'];
        var jqxhr = $.get( url, function(data) {
            console.log(data[0]['fields'])
            leadFormDetails.details = data[0]['fields'];
            document.getElementById("lead-form-details-loading").style.display = 'none';
            document.getElementById("lead-form-details").style.display = '';
        })
    })
});
$('#call-lead').click(function(){
    var url = '/api/v1/campaigns/make-call';
    postData = {
        "reference_number":$('#reference_number').val(),
        "campaign_id":campaignID,
        "caller_id":$("#call-manager-caller-id").val(),
        "lead_data":[]
    }
    var lead_data = document.getElementsByClassName('lead-call-data');
    for(var i = 0; i<lead_data.length; i++){
        postData['lead_data'].push({
            "field_name":$(lead_data[i]).attr('form-name'),
            "field_value":$(lead_data[i]).val(),
            "form_field_id":$(lead_data[i]).attr('form-id')
        })
    }
    console.log(postData);
    postToAPI(url, postData, 'POST', 'updateCallCampaigns');
});
try{
    document.getElementById('call-manager-body-loading').style.display = 'none';
    document.getElementById('call-manager-body').style.display = '';
}catch(error){}
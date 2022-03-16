try{
    document.getElementById('call-manager-body-loading').style.display = '';
    document.getElementById('call-manager-body').style.display = 'none';
}catch(error){}
calculateProgressBars();

var callCampaigns = new Vue({
    delimiters: ['[[', ']]'],
    el: '#call-manager-body',
    data: {
        campaigns:[]
    }
})

function updateCallCampaigns(){
    console.log('Update Call Campaigns');
    callCampaigns.campaigns = [];
    try{
        $("#call-manager-body").fadeOut();
        $("#call-manager-body").promise().done(function(){
            $("#call-manager-body-loading").fadeIn();
        });
    }catch(error){}
    var jqxhr = $.get( '/api/vici/campaigns', function(data) {
        console.log(data);
        callCampaigns.campaigns = data['data'];
    }).always(function(){
        try{
            $("#call-manager-body-loading").fadeOut();
            $("#call-manager-body-loading").promise().done(function(){
                $("#call-manager-body").fadeIn();
            });
        }catch(error){}
        setTimeout(function(){
            calculateProgressBars();
        },1000);
    });
}

updateCallCampaigns();

$('body').on('click','.control-campaign', function(){
    $("#call-manager-body").fadeOut();
    $("#call-manager-body").promise().done(function(){
        $("#call-manager-body-loading").fadeIn();
    });
    var status = $(this).attr("campaign-status");
    var campaign_id = $(this).attr("campaign-id");
    var post_data = {
        "campaign_id":campaign_id,
        "status":status
    }
    postToAPI('/api/vici/campaigns_control', post_data, 'POST', 'updateCallCampaigns');
});
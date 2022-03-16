try{
    document.getElementById('company-lead-summary-loading').style.display = '';
    document.getElementById('company-lead-summary').style.display = 'none';
}catch(error){}
var campaignid; 
var companyLeadSummary = new Vue({
    delimiters: ['[[', ']]'],
    el: '#company-lead-summary',
    data: {
        summary:{}
    }
})

function updateCompanyLeadSummary(){
    try{
        document.getElementById('company-lead-summary-loading').style.display = '';
        document.getElementById('company-lead-summary').style.display = 'none';
    }catch(error){}
    var camp_dates = getBuiltInDatesFull('today');
    var url = '/api/v1/lead/campaign-summary?from='+camp_dates[0]+' 00:00:00'+'&to='+camp_dates[1]+' 23:59:59';
    if(campaignid){
        url += '&campaignid='+campaignid;
    }
    console.log(url);
    var jqxhr = $.get( url, function(data) {
        companyLeadSummary.summary = data;
        try{
            document.getElementById('company-lead-summary-loading').style.display = 'none';
            document.getElementById('company-lead-summary').style.display = '';
        }catch(error){}
    });
}

$('body').on('change','.lead-campaigns', function(){
    console.log('Testing')
    campaignid = $(this).val();
    updateCompanyLeadSummary();
});

function getCampaignSpecificDataToday(campaign_id){
    var camp_dates = getBuiltInDatesFull('today');
    var url = '/api/v1/lead/campaign-summary?from='+camp_dates[0]+' 00:00:00'+'&to='+camp_dates[1]+' 23:59:59&campaignid='+campaign_id;
    console.log(url);
    calls_made = 0;
    var _id = 'xfer-body-'+campaign_id;
    var jqxhr = $.get( url, function(data) {
        _id = 'today-body-'+campaign_id;
        document.getElementById(_id).innerHTML = formatMoney(data['calls_made'], 0);
        _id = 'xfer-body-'+campaign_id;
        document.getElementById(_id).innerHTML = formatMoney(data['total_interested'], 0);
    });
}

function getCampaignSpecificDataHour(campaign_id){
    var camp_dates = getBuiltInDatesFull('today');
    var d = new Date();
    d.setMinutes(d.getMinutes() + d.getTimezoneOffset());
    var curr_hour = d.getHours();
    var cur_hours_str = String(curr_hour);
    if(curr_hour<10){
        cur_hours_str = '0'+cur_hours_str;
    }
    var url = '/api/v1/lead/campaign-summary?from='+camp_dates[0]+' '+curr_hour+':00:00'+'&to='+camp_dates[1]+' '+curr_hour+':59:59&campaignid='+campaign_id;
    console.log(url);
    calls_made = 0;
    var jqxhr = $.get( url, function(data) {
        var _id = 'hour-body-'+campaign_id;
        document.getElementById(_id).innerHTML = formatMoney(data['calls_made'], 0);
    });
}

function formatID(prefix, campaign_id){
    return prefix+campaign_id;
}
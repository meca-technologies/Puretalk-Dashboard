document.getElementById('campaign-breakdown-loading').style.display = '';
document.getElementById('campaign-breakdown').style.display = 'none';

var campaignCounts = new Vue({
    delimiters: ['[[', ']]'],
    el: '#campaign-breakdown',
    data: {
        campaignCounts:[],
        length:0
    }
})

function updateCampaignCounts(){
    var jqxhr = $.get( '/api/v1/campaigns/counts?limit=2000', function(data) {
        console.log(data);
        campaignCounts.campaignCounts = data;
        campaignCounts.length = data.length;
    }).always(function(){
        document.getElementById('campaign-breakdown-loading').style.display = 'none';
        document.getElementById('campaign-breakdown').style.display = '';
    });
}

updateCampaignCounts();
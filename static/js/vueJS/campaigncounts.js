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

var campaignCostBreakdown = new Vue({
    delimiters: ['[[', ']]'],
    el: '#cost-breakdown',
    data: {
        costBreakdown:[]
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
    var breakdown_dict = {};
    var count_campaign = 0;
    var max_campaign = 1;
    var today = getBuiltInDatesFull('today');
    var jqxhr = $.get( '/api/v1/campaigns', function(data) {
        max_campaign = data.length;
        for(var i = 0; i<data.length; i++){
            breakdown_dict[data[i]['id']] = {
                'name':data[i]['name'],
                'charge_amount':0,
                'time_taken':0
            }
        }
        for(var i = 0; i<data.length; i++){
            var campaign_id = data[i]['id'];
            //var url = '/api/v1/wallet/earnings_new?campaignid='+campaign_id+'&from=2022-01-24&to=2022-01-24';
            var url = '/api/v1/wallet/earnings_new?campaignid='+campaign_id+'&from='+today[0]+'&to='+today[0];
            var jqxhr = $.get( url, function(data) {
                try{
                    if(data[0]['charge_amount'] !== undefined){
                        breakdown_dict[data[0]['campaign_id']]['charge_amount'] = data[0]['charge_amount'];
                    }
                    if(data[0]['time_taken'] !== undefined){
                        breakdown_dict[data[0]['campaign_id']]['time_taken'] = data[0]['time_taken'];
                    }
                    console.log(breakdown_dict);
                }catch(error){}
                count_campaign+=1;
            })
        }
        var checkMe = setInterval(function(){
            if(count_campaign >= max_campaign){
                console.log('done counting');
                console.log(breakdown_dict);
                campaignCostBreakdown.costBreakdown = breakdown_dict;
                document.getElementById('cost-breakdown-loading').style.display = 'none';
                document.getElementById('cost-breakdown').style.display = '';
                clearInterval(checkMe);
            }
        }, 1000)
    });
}

updateCampaignCounts();
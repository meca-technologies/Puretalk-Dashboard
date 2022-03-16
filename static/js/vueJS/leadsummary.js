var campaignid;

try{
    document.getElementById('lead-summary-loading').style.display = '';
    document.getElementById('lead-summary').style.display = 'none';
}catch(error){}
var leadSummary = new Vue({
    delimiters: ['[[', ']]'],
    el: '#lead-summary',
    data: {
        summary:{}
    }
})

function updateLeadSummary(){
    try{
        document.getElementById('lead-summary-loading').style.display = '';
        document.getElementById('lead-summary').style.display = 'none';
    }catch(error){}
    var url = '/api/v1/leads/summary';
    if(campaignid){
        url = '/api/v1/leads/summary?campaignid='+campaignid;
    }
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        leadSummary.summary = data;
        document.getElementById('lead-summary-loading').style.display = 'none';
        document.getElementById('lead-summary').style.display = '';
    });
}

$('body').on('change','.lead-campaigns', function(){
    console.log('Testing')
    campaignid = $(this).val();
    updateLeadSummary();
});
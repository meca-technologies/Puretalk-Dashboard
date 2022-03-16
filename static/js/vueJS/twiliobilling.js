var twilioBilling = new Vue({
    delimiters: ['[[', ']]'],
    el: '#twilio-transaction-body',
    data: {
        transactions:[]
    }
})

var twilioSummary = new Vue({
    delimiters: ['[[', ']]'],
    el: '#twilio-summary-body',
    data: {
        total:0
    }
})

$('#company-body').change(function(){
    if($(this).val() != 'none'){
        document.getElementById('twilio-transaction-loading').style.display = '';
        document.getElementById('twilio-transaction-body').style.display = 'none';
        document.getElementById('twilio-summary-body').style.display = 'none';
        var url = '/api/v1/wallet/twilio?companyid='+$(this).val();
        var jqxhr = $.get( url, function(data) {
            twilioBilling.transactions = data;
            var total = 0;
            for(var i = 0; i<data.length; i++){
                if(!isNaN(parseFloat(data[i]['price']))){
                    console.log(parseFloat(data[i]['price']));
                    total += parseFloat(data[i]['price']);
                }
            }
            twilioSummary.total = total;
            document.getElementById('twilio-transaction-loading').style.display = 'none';
            document.getElementById('twilio-transaction-body').style.display = '';
            document.getElementById('twilio-summary-body').style.display = '';
        })
    }
});
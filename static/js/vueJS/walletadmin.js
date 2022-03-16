document.getElementById('wallet-summary-body').style.display = 'none';
var wallet_table;
var walletDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#wallet-summary-body',
    data: {
        details:{
            "paid_balance": 0.0,
            "refunded_balance": 0.0,
            "voided_balance": 0.0
        }
    }
})

var walletTransactions = new Vue({
    delimiters: ['[[', ']]'],
    el: '#wallet-transaction-body',
    data: {
        transactions:[]
    }
})

$("#wallet-filter-report").click(function(){
    //walletDetails.details.paid_balance = 1;
    //document.getElementById('wallet-summary-body').style.display = 'none';
    document.getElementById('wallet-summary-body-loading').style.display = '';
    document.getElementById('wallet-transaction-body').style.display = 'none';
    var params = "";
    if($("#from-date").val()){
        params+="&from="+$("#from-date").val();
    }
    if($("#to-date").val()){
        params+="&to="+$("#to-date").val();
    }
    if($("#tran-type").val() != 'none'){
        params+="&type="+$("#tran-type").val();
    }
    try{
        wallet_table.destroy()
    }catch(error){}
    var url = '/api/v1/wallet?companyid='+$("#company-body").val()+params;
    console.log(url);
    var jqxhr = $.get( url, function(data) {
        //smoothTransition(data);
        console.log(typeof(data));
        walletTransactions.transactions = data;
    }).always(function(){
        setTimeout(function(){
            wallet_table = $('#wallet-transaction-table').DataTable({
                "order": [[ 4, "desc" ]],
                "lengthMenu": [[-1, 10, 25, 50], ["All", 10, 25, 50]],
            });
            document.getElementById('wallet-summary-body-loading').style.display = 'none';
            document.getElementById('wallet-summary-body').style.display = '';
            document.getElementById('wallet-transaction-body').style.display = '';
        }, 1000);
    });
})

$('#company-body').change(function(){
    getTransactions(this);
});

function getTransactions(_this){
    $('#add-credit').modal('hide');
    //walletDetails.details.paid_balance = 1;
    //document.getElementById('wallet-summary-body').style.display = 'none';
    document.getElementById('wallet-summary-body-loading').style.display = '';
    document.getElementById('wallet-summary-body').style.display = 'none';
    document.getElementById('wallet-transaction-body').style.display = 'none';
    console.log($(_this).val());
    try{
        wallet_table.destroy()
    }catch(error){}
    if($(_this).val() != 'none'){
        //var url = '/api/v1/wallet/balance?companyid='+$(this).val();
        //var jqxhr = $.get( url, function(data) {
        //    
        //}).always(function(){
        //    document.getElementById('wallet-summary-body').style.display = '';
        //});

        var url = '/api/v1/wallet?companyid='+$(_this).val();
        var jqxhr = $.get( url, function(data) {
            smoothTransition(data);
            //walletDetails.details.paid_balance = maxVal;
            //walletDetails.details = data;
            walletTransactions.transactions = data;
        }).always(function(){
            setTimeout(function(){
                wallet_table = $('#wallet-transaction-table').DataTable({
                    "order": [[ 4, "desc" ]],
                    "lengthMenu": [[-1, 10, 25, 50], ["All", 10, 25, 50]],
                });
                document.getElementById('wallet-summary-body-loading').style.display = 'none';
                document.getElementById('wallet-summary-body').style.display = '';
                document.getElementById('wallet-transaction-body').style.display = '';
            }, 1000);
        });
    }
}

$("#wallet-add-credit").click(function(){
    var memo = $("#credit-memo").val()
    if (memo == ''){
        memo = null;
    }
    var postData = {
        "company_id":$("#company-body").val(),

        "type":"paid",
        "amount":parseFloat($("#credit-to-add").val()),
        "memo":memo
    }
    console.log(postData);
    postToAPI('/api/v1/wallet', postData, 'POST', 'updateWalletBalance');
});
$("#wallet-add-funds").click(function(){
    var memo = $("#memo").val()
    if (memo == ''){
        memo = null;
    }
    var postData = {
        "company_id":$("#company-body").val(),
        "customer_name":$("#customer-name").val(),
        "customer_email":$("#customer-email").val(),
        "customer_address":$("#customer-address").val(),
        "customer_city":$("#customer-city").val(),
        "customer_state":$("#customer-state").val(),
        "customer_zip":$("#customer-zip").val(),
        "customer_country":$("#customer-country").val(),

        "card_number":$("#card-number").val().replace(/\D/g,''),
        "card_exp_month":String($("#card-exp").val().replace(/\D/g,'')).substring(0,2),
        "card_exp_year":"20"+String($("#card-exp").val().replace(/\D/g,'')).substring(2,4),
        "card_cvc":$("#card-cvc").val().replace(/\D/g,''),

        "type":"paid",
        "amount":parseFloat($("#funds-to-add").val()),
        "memo":memo
    }
    console.log(postData);
    //postToAPI('/api/v1/stripe/charge', postData, 'POST', 'updateWalletBalance');
    
    document.getElementById("alert-holder").style.display = '';
    $.ajax({
        type: 'POST',
        url: '/api/v1/stripe/charge',
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: JSON.stringify(postData),
        success: function(data){
            console.log("data");
            console.log(data);
            if(data['Message'] == 'Success'){
                $('#card-number').removeClass('border');
                $('#card-number').removeClass('border-danger');
                alerts.alerts.push({
                    "status":"success",
                    "message":"Charge was successful"
                })
                var parent = $('#card-number').parent().get( 0 );
                parent = $(parent).parent().get( 0 );
                parent.style.height = '51px';
                $('#company-body').change();
            }
            else if(data['Message'] == 'Card number was not valid!'){
                alerts.alerts.push({
                    "status":"danger",
                    "message":data['Message']
                })
                var parent = $('#card-number').parent().get( 0 );
                parent = $(parent).parent().get( 0 );
                parent.style.height = '80px';
                $('#card-number').addClass('border');
                $('#card-number').addClass('border-danger');
            }
        },
        error: function(data){
            console.log('FAILURE');
        }
    });
})
$("#card-number").keydown(function(){
    var number = $(this).val().replace(/\D/g,'');
    var number_split = number.split('');
    var new_val = '';
    for(var i = 0; i<number_split.length; i++){
        if(i == 4 || i == 8 || i == 12 || i == 16){
            new_val += '-';
        }
        new_val += number_split[i];
    }
    $(this).val(new_val);
});

$("#card-exp").keydown(function(){
    var number = $(this).val().replace(/\D/g,'');
    var number_split = number.split('');
    var new_val = '';
    for(var i = 0; i<number_split.length; i++){
        if(i == 2 || i == 8 || i == 12 || i == 16){
            new_val += '/';
        }
        new_val += number_split[i];
    }
    $(this).val(new_val);
});

$('body').on('click','.void-transaction', function(){
    var updateData = {
        "id":$(this).attr('transaction-id'),
        "type":"voided"
    }
    postToAPI('/api/v1/wallet', updateData, 'PUT', 'updateWalletBalance');
});

function goBetweenNumbers(min, max, rate){
    if(min < 1){
        min = 1;
    }
    var calcRate = (max-min)/rate;
    return calcRate;
}

function smoothTransition(data){
    var currVal = walletDetails.details.paid_balance;
    try{
        var maxVal = data.reduce(myFunc);
    }catch(error){
        var maxVal = 0;
    }
    if(typeof(maxVal) == 'object'){
        maxVal = data[0]['amount'];
    }
    console.log(maxVal)
    var rate = goBetweenNumbers(currVal, maxVal, 100);
    var diff = Math.abs(currVal-maxVal);
    if(rate < .3){
        if(diff>2){
            if(rate > 0){
                rate = 10;
            }
            else{
                rate = -10;
            }
        }
        else{
            if(rate > 0){
                rate = .1;
            }
            else{
                rate = -.1;
            }
        }
    }
    document.getElementById('wallet-summary-body').style.display = '';
    if(currVal != maxVal){
        if(maxVal > currVal){
            var x = setInterval(function(){
                currVal+=rate;
                walletDetails.details.paid_balance = currVal;
                if(currVal>=maxVal){
                    walletDetails.details.paid_balance = maxVal;
                    console.log(walletDetails.details.paid_balance);
                    clearInterval(x);
                }
            }, 10);
        }
        else{
            var x = setInterval(function(){
                currVal+=rate;
                walletDetails.details.paid_balance = currVal;
                if(currVal<=maxVal){
                    walletDetails.details.paid_balance = maxVal;
                    console.log(walletDetails.details.paid_balance);
                    clearInterval(x);
                }
            }, 20);
        }
    }
}

function myFunc(total, num) {
    //console.log(typeof(total));
    //console.log(total);
    //console.log(typeof(num));
    //console.log(num);
    total_amount = total
    if(typeof(total) == 'string'){
        total_amount = parseFloat(total)
    }
    else if(typeof(total) == 'object'){
        total_amount = parseFloat(total['amount'])
    }
    amount = num["type"] == "paid"?parseFloat(num["amount"]):parseFloat(num["amount"])*-1;
    //console.log(String(total_amount) + "+" + String(amount));
    //console.log('\n');
    return total_amount + amount;
}
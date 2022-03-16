document.getElementById('wallet-summary-body').style.display = 'none';
var walletDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#wallet-summary-body',
    data: {
        details:{}
    }
})

var walletTransactions = new Vue({
    delimiters: ['[[', ']]'],
    el: '#wallet-transaction-body',
    data: {
        transactions:[]
    }
})

var walletTable;

function getWallet(){
    try{
        walletTable.destroy()
    }catch(error){}
    try{
        $("#wallet-summary-body").fadeOut();
        $("#wallet-transaction").fadeOut();
        $("#wallet-summary-body").promise().done(function(){
            $("#wallet-summary-body-loading").fadeIn();
        });
    }catch(error){}
    var url = '/api/vici/billing';
    var jqxhr = $.get( url, function(data) {
        walletDetails.details = data;
        walletTransactions.transactions = data['data'];
        console.log(data['data'])
    }).always(function(){
        setTimeout(function(){
            try{
                $("#wallet-summary-body-loading").fadeOut();
                $("#wallet-summary-body-loading").promise().done(function(){
                    $("#wallet-summary-body").fadeIn();
                    $("#wallet-transaction-body").fadeIn();
                });
            }catch(error){}
            //try{
            walletTable = document.getElementById("wallet-transaction-table");
            console.log(walletTable.nodeName);
            if(walletTable.nodeName == 'TABLE'){
                walletTable = $('#wallet-transaction-table').DataTable({
                    "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
                    "language": {
                        "paginate": {
                            "previous": "<<",
                            "next": ">>"
                        }
                    },
                    initComplete: function() {
                        $(this.api().table().container()).find('input[type="search"]').parent().wrap('<form>').parent().attr('autocomplete','off').css('overflow','hidden').css('margin','auto');
                    }   
                });
            }
            //}catch(error){}
        },1000)
    });
}

getWallet();


$("#wallet-add-funds").click(function(){
    var memo = $("#memo").val();
    document.getElementById("stripe-charge-loading").style.display = "";
    document.getElementById("stripe-charge").style.display = "none";
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
        "amount":$("#funds-to-add").val(),
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
                $('#add-funds').modal('hide');
                getWallet();
                document.getElementById("stripe-charge-loading").style.display = "none";
                document.getElementById("stripe-charge").style.display = "";
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
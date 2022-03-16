var paymentSettings = new Vue({
    delimiters: ['[[', ']]'],
    el: '#payment-body',
    data: {
        settings:{}
    }
})

function updatePaymentSettings(){
    var url = '/api/v1/payment-settings';
    var jqxhr = $.get( url, function(data) {
        paymentSettings.settings = data;
    })
}

updatePaymentSettings();

$("#save-payment-settings").click(function(){
    var updateData = {}
    try{if($('[name="paypal_client_id"]').is(":visible")){updateData['paypal_client_id'] = $('[name="paypal_client_id"]').val();}}catch(error){}
    try{if($('[name="paypal_secret"]').is(":visible")){updateData['paypal_secret'] = $('[name="paypal_secret"]').val();}}catch(error){}
    try{if($('[name="paypal_mode"]').is(":visible")){updateData['paypal_mode'] = $('[name="paypal_mode"]').val();}}catch(error){}
    
    try{if($('[name="stripe_api_key"]').is(":visible")){updateData['stripe_api_key'] = $('[name="stripe_api_key"]').val();}}catch(error){}
    try{if($('[name="stripe_api_secret"]').is(":visible")){updateData['stripe_api_secret'] = $('[name="stripe_api_secret"]').val();}}catch(error){}
    try{if($('[name="stripe_webhook_key"]').is(":visible")){updateData['stripe_webhook_key'] = $('[name="stripe_webhook_key"]').val();}}catch(error){}
    try{if($('[name="stripe_status"]').is(":visible")){updateData['stripe_status'] = $('[name="stripe_status"]').val() == 'on'?true:false;}}catch(error){}

    try{if($('[name="razorpay_key"]').is(":visible")){updateData['razorpay_key'] = $('[name="razorpay_key"]').val();}}catch(error){}
    try{if($('[name="razorpay_secret"]').is(":visible")){updateData['razorpay_secret'] = $('[name="razorpay_secret"]').val();}}catch(error){}
    try{if($('[name="razorpay_webhook_secret"]').is(":visible")){updateData['razorpay_webhook_secret'] = $('[name="razorpay_webhook_secret"]').val();}}catch(error){}

    try{if($('[name="paystack_client_id"]').is(":visible")){updateData['paystack_client_id'] = $('[name="paystack_client_id"]').val();}}catch(error){}
    try{if($('[name="paystack_secret"]').is(":visible")){updateData['paystack_secret'] = $('[name="paystack_secret"]').val();}}catch(error){}
    try{if($('[name="paystack_merchant_email"]').is(":visible")){updateData['paystack_merchant_email'] = $('[name="paystack_merchant_email"]').val();}}catch(error){}

    try{if($('[name="mollie_api_key"]').is(":visible")){updateData['mollie_api_key'] = $('[name="mollie_api_key"]').val();}}catch(error){}

    try{if($('[name="authorize_api_login_id"]').is(":visible")){updateData['authorize_api_login_id'] = $('[name="authorize_api_login_id"]').val();}}catch(error){}
    try{if($('[name="authorize_transaction_key"]').is(":visible")){updateData['authorize_transaction_key'] = $('[name="authorize_transaction_key"]').val();}}catch(error){}
    try{if($('[name="authorize_signature_key"]').is(":visible")){updateData['authorize_signature_key'] = $('[name="authorize_signature_key"]').val();}}catch(error){}
    try{if($('[name="authorize_environment"]').is(":visible")){updateData['authorize_environment'] = $('[name="authorize_environment"]').val();}}catch(error){}

    console.log(updateData);
    postToAPI('/api/v1/payment-settings', updateData, 'PUT', 'updatePaymentSettings');
});

var globalSettings = new Vue({
    delimiters: ['[[', ']]'],
    el: '#global-body',
    data: {
        settings:{}
    }
})

function updateGlobalSettings(){
    var url = '/api/v1/global-settings';
    var jqxhr = $.get( url, function(data) {
        globalSettings.settings = data;
    })
}

updateGlobalSettings();
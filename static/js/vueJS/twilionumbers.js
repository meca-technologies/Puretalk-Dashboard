var twilioNumbers = new Vue({
    delimiters: ['[[', ']]'],
    el: '#phone-numbers',
    data: {
        available_numbers:[]
    }
})

var twilioPurchasableNumbers = new Vue({
    delimiters: ['[[', ']]'],
    el: '#phone-number-add',
    data: {
        purchasable_numbers:[]
    }
})

var twilioNumberDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#phone-number-edit',
    data: {
        details:{},
        virtual_agents:[]
    }
})

function getAvailableNumbers(){
    console.log('GET NUMBERS');
    $(".sidebar-transparent").click();
    $("#phone-number-add").modal('hide');
    document.getElementById("phone-numbers-loading").style.display = '';
    document.getElementById("phone-numbers").style.display = 'none';

    document.getElementById("phone-number-add-loading").style.display = '';
    document.getElementById("phone-number-add-body").style.display = 'none';

    var url = '/api/v1/twilio/available_numbers';
    var jqxhr = $.get( url, function(data) {
        twilioNumbers.available_numbers = data['available_numbers'];
        twilioPurchasableNumbers.purchasable_numbers = data['purchasable_numbers'];
        document.getElementById("phone-numbers-loading").style.display = 'none';
        document.getElementById("phone-numbers").style.display = '';

        document.getElementById("phone-number-add-loading").style.display = 'none';
        document.getElementById("phone-number-add-body").style.display = '';
    });
}

getAvailableNumbers();

$("#purchase-filter").click(function(){
    document.getElementById("phone-number-add-loading").style.display = '';
    document.getElementById("phone-number-add-body").style.display = 'none';

    var url = '/api/v1/twilio/available_numbers?areacode='+$("#area-code-filter").val();
    var jqxhr = $.get( url, function(data) {
        twilioNumbers.available_numbers = data['available_numbers'];
        twilioPurchasableNumbers.purchasable_numbers = data['purchasable_numbers'];

        document.getElementById("phone-number-add-loading").style.display = 'none';
        document.getElementById("phone-number-add-body").style.display = '';
    });
})

$('body').on('click','.purchase-number', function(){
    document.getElementById("phone-number-add-loading").style.display = '';
    document.getElementById("phone-number-add-body").style.display = 'none';
    console.log($(this).attr("phone"));

    var post_data = {
        "phone_number":$(this).attr("phone")
    }
    
    postToAPI('/api/v1/twilio/available_numbers', post_data, 'POST', 'getAvailableNumbers');
});

$('body').on('click','.phone-number-edit', function(){
    var url = '/api/v1/twilio/available_numbers?phoneid='+$(this).attr("phone-id");
    var jqxhr = $.get( url, function(data) {
        twilioNumberDetails.details = data;
    });
    var jqxhr = $.get( '/api/v1/virtual-agents?limit=2000', function(data) {
        console.log(data);
        twilioNumberDetails.virtual_agents = data;
    })
});

$("#edit-phone-number").click(function(){
    var post_data = {
        "id":$("#edit-phone-id").val(),
        "phone_sid":$("#edit-phone-sid").val(),
        "friendly_name":$("#edit-phone-name").val(),
        "virtual_agent_id":$("#edit-virtual-agent").val(),
    }
    console.log(post_data);
    postToAPI('/api/v1/twilio/available_numbers', post_data, 'PUT', 'getAvailableNumbers');
})


var phone_id = null;
var phone_sid = null;
$('body').on('click','.phone-number-delete', function(){
    phone_id = $(this).attr("phone-id");
    phone_sid = $(this).attr("phone-sid");
});

$("#phone-delete-conf").click(function(){
    var delete_data = {
        "id":phone_id,
        "phone_sid":phone_sid
    }
    console.log(delete_data);
    postToAPI('/api/v1/twilio/available_numbers', delete_data, 'DELETE', 'getAvailableNumbers');
})
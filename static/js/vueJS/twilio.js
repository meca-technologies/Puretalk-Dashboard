var twilioVue = new Vue({
    delimiters: ['[[', ']]'],
    el: '#product-table',
    data: {
        products:[]
    }
})

var productDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#product-view-body',
    data: {
        details:[]
    }
})

$('body').on('change','#company-body', function(){
    var url = '/api/v1/twilio/shakenstirs?companyid='+$(this).val();
    console.log(url);
    var jqxhr = $.get( url, function(data) {
        twilioVue.products = data;
    });
});

$('body').on('click','.product-view', function(){
    document.getElementById("product-view-loading").style.display = '';
    document.getElementById("product-view-body").style.display = 'none';
    var url = '/api/v1/twilio/shakenstirs/phones?companyid='+$('#company-body').val()+'&profileid='+$(this).attr('product-id');
    console.log(url);
    var jqxhr = $.get( url, function(data) {
        productDetails.details = data;
        document.getElementById("product-view-loading").style.display = 'none';
        document.getElementById("product-view-body").style.display = '';
    });
})
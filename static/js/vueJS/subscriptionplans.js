var subscriptionPlans = new Vue({
    delimiters: ['[[', ']]'],
    el: '#plan-body',
    data: {
        subscriptionPlans:[]
    }
})
var planDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#plan-edit',
    data: {
        details:{}
    }
})

function updatePlans(){
    var jqxhr = $.get( '/api/v1/subscription-plans?limit=2000', function(data) {
        console.log(data);
        subscriptionPlans.subscriptionPlans = data;
    })
}


$('body').on('click','.plan-edit', function(){
    var url = '/api/v1/subscription-plans?subid='+$(this).attr('sub-id');
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        planDetails.details = data[0];
    });
});

updatePlans();
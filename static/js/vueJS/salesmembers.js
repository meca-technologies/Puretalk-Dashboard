var salesMembers = new Vue({
    delimiters: ['[[', ']]'],
    el: '#sales-member-body',
    data: {
        users:[]
    }
})

var salesMemberDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#sales-member-edit',
    data: {
        details:{}
    }
})

function updateSalesMembers(){
    var jqxhr = $.get( '/api/v1/sales-members?limit=2000', function(data) {
        console.log(data);
        salesMembers.users = data;
    })
}

$('body').on('click','.user-edit', function(){
    var url = '/api/v1/sales-members?userid='+$(this).attr('user-id');
    var jqxhr = $.get( url, function(data) {
        console.log(data[0])
        salesMemberDetails.details = data[0];
    });
});

updateSalesMembers();
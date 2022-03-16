document.getElementById('follow-up-body-loading').style.display = '';
document.getElementById('follow-up-body').style.display = 'none';

var followUps = new Vue({
    delimiters: ['[[', ']]'],
    el: '#follow-up-body',
    data: {
        followUps:[],
        length:0
    }
})

function updatefollowUps(){
    var jqxhr = $.get( '/api/v1/follow-calls?limit=2000', function(data) {
        console.log(data);
        followUps.followUps = data;
        followUps.length = data.length;
    }).always(function(){
        document.getElementById('follow-up-body-loading').style.display = 'none';
        document.getElementById('follow-up-body').style.display = '';
    });
}

updatefollowUps();
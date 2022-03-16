var agentsDashboard = new Vue({
    delimiters: ['[[', ']]'],
    el: '#agent-dashboard-body',
    data: {
        details:{}
    }
})

function getHooks(){
    var jqxhr = $.get( '/agent/hooks', function(data) {
        if(data['Message'] == "Success"){
            agentsDashboard.details = data['details']['details']
        }
    });
}

getHooks();

setInterval(function(){
    getHooks();
}, 10000)
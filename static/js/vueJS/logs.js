document.getElementById('logs-loading').style.display = 'none';
document.getElementById('logs-body').style.display = '';

var logsVue = new Vue({
    delimiters: ['[[', ']]'],
    el: '#logs-body',
    data: {
        logs:[],
        users:[]
    }
})


var logDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#logs-view-body',
    data: {
        details:{}
    }
})

var log_table;

$("#submit-logs").click(function(){
    document.getElementById('logs-loading').style.display = '';
    document.getElementById('logs-body').style.display = 'none';

    var url = '/api/v1/users/logs?limit=2000';
    if($("#users-id").val() != 'none'){
        url += '&userid='+$("#users-id").val();
    }
    if($("#from-date").val() && $("#from-date").val() !== undefined){
        url += '&from='+formatUTCDateTime($("#from-date").val());
    }
    if($("#to-date").val() && $("#to-date").val() !== undefined){
        url += '&to='+formatUTCDateTime($("#to-date").val());
    }
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        logsVue.logs = data;
        try{
            log_table.destroy();
        }catch(error){}
    }).always(function(){
        setTimeout(function(){
            try{
                log_table = $('#log-table').DataTable({
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
            }catch(error){}
            document.getElementById('logs-loading').style.display = 'none';
            document.getElementById('logs-body').style.display = '';
        }, 1000)
    });
})

var jqxhr = $.get( '/api/v1/users/all?limit=2000', function(data) {
    logsVue.users = data;
}).always(function(){
    document.getElementById('logs-loading').style.display = 'none';
    document.getElementById('logs-body').style.display = '';
});

$('body').on('click','.log-view', function(){
    document.getElementById('logs-view-loading').style.display = '';
    document.getElementById('logs-view-body').style.display = 'none';
    var url = '/api/v1/users/logs?logid='+$(this).attr('log-id');
    var jqxhr = $.get( url, function(data) {
        logDetails.details = data[0];
        document.getElementById('logs-view-loading').style.display = 'none';
        document.getElementById('logs-view-body').style.display = '';
    });
});
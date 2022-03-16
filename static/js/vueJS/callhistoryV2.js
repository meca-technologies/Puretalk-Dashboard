var skip = 0;
var limit = 10000;
var currPage = 1;
try{
    sortColumn = $('#lead-table').attr('sort-col');
}catch(error){
    sortColumn = 1
}

try{
    sortStyle = $('#lead-table').attr('sort-style');
}catch(error){
    sortStyle = 'asc';
}

try{
    pageLength = $('#lead-table').attr('page-length');
}catch(error){
    pageLength = 5;
}

try{
    hideColsRaw = $('#lead-table').attr('hide-col');
    hideCols = hideColsRaw.split(',');
}catch(error){
    hideCols = [];
}

try{
    document.getElementById('lead-table-loading').style.display = 'none';
    document.getElementById('lead-table').style.display = '';
}catch(error){}

var leadData = [];

var leadTable;
document.getElementById("lead-table").style.display = '';
/*leadTable = $('#lead-table').DataTable({
    "order": [[ parseInt(sortColumn), sortStyle ]],
    "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
    "pageLength": parseInt(pageLength),
    "language": {
      "paginate": {
        "previous": "<<",
        "next": ">>"
      }
    }
});*/
var leads = new Vue({
    delimiters: ['[[', ']]'],
    el: '#leads-body',
    data: {
        leads:[{
            "Email": "-",
            "First_Name": "-",
            "Last_Name": "-",
            "Phone_No": "-",
            "campaign_name": "-",
            "id": '-',
            "interested": null,
            "lead_data": [],
            "recordings": [],
            "reference_number": "-",
            "status": "-"
        }]
    }
})
var leadDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#lead-details',
    data: {
        details:{},
        lead_details:{}
    }
})

$("#lead-filter-report").click(function(){
    $(".lead-campaigns").change();
})

$(".lead-campaigns").change(function(){
    getLeads();
    if($("#from-date").val() != '' && $("#to-date").val() != ''){
        var d = new Date($("#from-date").val());
        var formatted_from = formatDate(d);
        
        var d = new Date($("#to-date").val());
        var formatted_to = formatDate(d);
    }
    else{
        var d = new Date('2021-01-01');
        var formatted_from = formatDate(d);
        
        var d = new Date('2031-01-01');
        var formatted_to = formatDate(d);
    }
    

    updateSummary(formatted_from, formatted_to);
});


var leadsTable;
function getLeads(){
    try{
        leadsTable.destroy()
    }catch(error){}
    try{        
        $("#lead-table-loading").fadeIn();
        $("#lead-table-loading").promise().done(function(){
            $("#lead-table").fadeOut();
        });
    }catch(error){}
    var url = '/api/vici/call_logs?campaign_id='+$("#campaign-body").val()+'&offset='+String(skip)+'&limit='+String(limit);
    if($("#lead-status").val() != 'none'){
        url += '&status='+$("#lead-status").val();
    }
    //if($("#lead-interested").val() != 'none'){
    //    url += '&interested='+$("#lead-interested").val();
    //}
    if($("#from-date").val() != '' && $("#to-date").val() != ''){
        var from_date = new Date($("#from-date").val());
        var from_date_str = formatDate(from_date) + ' ' + addZero(from_date.getHours()) + ':' + addZero(from_date.getMinutes())+':' + addZero(from_date.getSeconds());
        
        var to_date = new Date($("#to-date").val());
        var to_date_str = formatDate(to_date) + ' ' + addZero(to_date.getHours()) + ':' + addZero(to_date.getMinutes())+':' + addZero(to_date.getSeconds());

        url += '&from='+from_date_str;
        url += '&to='+to_date_str;
    }
    console.log(url);
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        leads.leads = data['data'];
        leadData = data;
        document.getElementById("lead-table").style.display = '';
    }).always(function(){
        try{
            document.getElementById('lead-table-loading').style.display = 'none';
            document.getElementById('lead-table').style.display = '';
        }catch(error){}
        setTimeout(function(){
            try{
                leadsTable = document.getElementById("lead-table");
                console.log(leadsTable.nodeName);
                if(leadsTable.nodeName == 'TABLE'){
                    leadsTable = $('#lead-table').DataTable({
                        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
                        "pageLength": parseInt(pageLength),
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
                    for(var i = 0; i<hideCols.length; i++){
                        console.log(hideCols[i])
                        leadsTable.column(parseInt(hideCols[i])).visible(false);
                        document.getElementById("lead-table").style.width = "100%";
                    }
                }
            }catch(error){}
        },1000)
    });
}

$('body').on('click','.lead-page', function(){
    currPage = parseInt($(this).attr("pagenum"));
    skip = (currPage-1) * limit;
    $(".lead-campaigns").change();
});

$('body').on('click','.incr-page', function(){
    var incr = parseInt($(this).attr("pagenum"));
    currPage -= incr;
    skip = (currPage-1) * limit;
    $(".lead-campaigns").change();
});

$('body').on('click','.lead-details', function(){
    var url = '/api/vici/call_logs?lead_id='+$(this).attr('lead-id');
    console.log(url);
    try{
        document.getElementById('lead-details-body-loading').style.display = '';
        document.getElementById('lead-details-body').style.display = 'none';
    }catch(error){}
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        for(var i = 0; i<data['data'].length; i++){
            data['data'][i]['location'] = '#';
        }
        leadDetails.details = data;
        console.log(leadDetails.details['data']);
        for(var i = 0; i<leadDetails.details['data'].length; i++){
            console.log(leadDetails.details['data'][i]);
            var url = '/api/vici/recordings?vicidial_id='+leadDetails.details['data'][i]['uniqueid'];
            console.log(url);
            var index = i;
            var jqxhr = $.get( url, function(data) {
                console.log(data['data'][0]['location']);
                leadDetails.details['data'][index].location = data['data'][0]['location'];
                console.log(leadDetails.details['data']);
            })
        }
        setTimeout(function(){
            try{
                document.getElementById('lead-details-body-loading').style.display = 'none';
                document.getElementById('lead-details-body').style.display = '';
            }catch(error){}
        }, 1000)
    })
    var url = '/api/vici/leads?lead_id='+$(this).attr('lead-id');
    console.log(url);
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        leadDetails.lead_details = data['data'][0];
    })
});

$('#export-history').click(function(){
    var csv = 'lead id,reference number,last disposition,total duration,call attempt,call duration,call recording\n';
    for(var i = 0; i<leadData.length; i++){
        var lead = leadData[i];
        csv += String(lead.id) + ',' + String(lead.reference_number) + ','+ String(lead.status) + ','+ String(lead.time_taken) + ',call attempt,call duration,call recording\n';
        for(var j = 0; j<lead['call_logs'].length; j++){
            callLog = lead['call_logs'][j];
            console.log
            try{
                recording = lead['recordings'][j]['recording_link'];
            }catch(error){
                recording = '';
            }
            csv += ',,,,' + String(callLog['cl_attempted_by']) + ',' + String(callLog['cl_time_taken']) + ',' + String(recording) + '\n';
        }
        csv += '\n'
    }
    console.log(csv);
    var hiddenElement = document.createElement('a');
    hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
    hiddenElement.target = '_blank';
    hiddenElement.download = 'call-history.csv';
    hiddenElement.click();
})

/*$('body').on('click','.lead-call', function(){
    var url = '/api/v1/campaigns/make-call';
    postData = {
        "reference_number":$(this).attr('reference'),
        "campaign_id":$(this).attr('campaign-id'),
        "lead_id":$(this).attr('lead-id')
    }
    postToAPI(url, postData, 'POST', 'doNothing');
});*/
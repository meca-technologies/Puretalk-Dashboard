const urlSearchParams = new URLSearchParams(window.location.search);
const params = Object.fromEntries(urlSearchParams.entries());
var skip = 0;
var limit = 100;
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

try{
    if(params.campaignid !== undefined){
        $("#campaign-body").val(params.campaignid);
        getLeads();
        //$(".lead-campaigns").change();
        $("#campaign-body").change();
    }
    else{
        console.log("trigger change");
        updateLeadSummary();
        updateCompanyLeadSummary();
    }
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
        details:{}
    }
})

$("#lead-filter-report").click(function(){
    $(".lead-campaigns").change();
})

$(".lead-campaigns").change(function(){
    getLeads()
});

$('body').on('click','.lead-delete', function(){
    var url = '/api/v1/leads';
    postData = {
        "id":$(this).attr('lead-id')
    }
    postToAPI(url, postData, 'DELETE', 'getLeads');
});

function getLeads(){
    try{
        document.getElementById('lead-table-loading').style.display = '';
        document.getElementById('lead-table').style.display = 'none';
    }catch(error){}
    var url = '/api/v1/leads?campaignid='+$("#campaign-body").val()+'&skip='+String(skip)+'&limit='+String(limit);
    if($("#lead-status").val() != 'none'){
        url += '&status='+$("#lead-status").val();
    }
    if($("#lead-interested").val() != 'none'){
        url += '&interested='+$("#lead-interested").val();
    }
    if($("#from-date").val() != '' && $("#to-date").val() != ''){
        url += '&from='+$("#from-date").val();
        url += '&to='+$("#to-date").val();
    }
    console.log(url);
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        leads.leads = data;
        leadData = data;
        document.getElementById("lead-table").style.display = '';
        try{
            var numPages = parseInt(data[0]['max_documents']/limit);
            var paginationHTML = '<li class="page-item incr-page" pagenum="1"><a class="page-link">&lt;&lt;</a></li>';
            if(currPage>2){
                paginationHTML += '<li class="page-item lead-page" pagenum="1"><a class="page-link">1</a></li>';
                if(numPages>1){
                    paginationHTML += '<li class="page-item lead-page" pagenum="2"><a class="page-link">2</a></li>';
                    paginationHTML += '<li>...</li>';
                }
            }
            else{
                if(currPage==1){
                    paginationHTML += '<li class="page-item active lead-page" pagenum="1"><a class="page-link">1</a></li>';
                    if(numPages>1){
                        paginationHTML += '<li class="page-item lead-page" pagenum="2"><a class="page-link">2</a></li>';
                    }
                }
                else{
                    paginationHTML += '<li class="page-item lead-page" pagenum="1"><a class="page-link">1</a></li>';
                    if(numPages>1){
                        paginationHTML += '<li class="page-item active lead-page" pagenum="2"><a class="page-link">2</a></li>';
                    }
                }
            }
            for(var i = 3; i<numPages; i++){
                if(numPages>10){
                    if(i>currPage-2 && i<currPage+2){
                        if(i==currPage){
                            paginationHTML += '<li class="page-item active lead-page" pagenum="'+String(i)+'"><a class="page-link">'+String(i)+'</a></li>';
                        }
                        else{
                            paginationHTML += '<li class="page-item lead-page" pagenum="'+String(i)+'"><a class="page-link">'+String(i)+'</a></li>';
                        }
                    }
                }
                else{
                    paginationHTML += '<li class="page-item lead-page" pagenum="'+String(i)+'"><a class="page-link">'+String(i)+'</a></li>';
                }
            }
            if(numPages>10 && (numPages-currPage)>2 && numPages>1){
                paginationHTML += '<li>...</li>';
            }
            
            if(numPages>1){
                if(currPage==numPages){
                    paginationHTML += '<li class="page-item active lead-page" pagenum="'+String(numPages)+'"><a class="page-link">'+String(numPages)+'</a></li>';
                }
                else{
                    paginationHTML += '<li class="page-item lead-page" pagenum="'+String(numPages)+'"><a class="page-link">'+String(numPages)+'</a></li>';
                }
            }
            paginationHTML += '<li class="page-item incr-page" pagenum="-1"><a class="page-link">&gt;&gt;</a></li>';
            document.getElementById("leads-table-pagination").innerHTML = paginationHTML;
        }catch(error){}
    }).always(function(){
        try{
            document.getElementById('lead-table-loading').style.display = 'none';
            document.getElementById('lead-table').style.display = '';
        }catch(error){}
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
    var url = '/api/v1/leads?campaignid='+$(this).attr('campaign-id')+'&leadid='+$(this).attr('lead-id');
    document.getElementById("lead-details-body").style.display = "none";
    document.getElementById("lead-details-loading").style.display = "";
    console.log(url);
    var jqxhr = $.get( url, function(data) {
        console.log(data[0]);
        leadDetails.details = data[0];
        document.getElementById("lead-details-body").style.display = "";
        document.getElementById("lead-details-loading").style.display = "none";
        setTimeout(function(){
            document.getElementById("recording-audio").load();
        },1000)
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

$('body').on('click','.lead-call', function(){
    var url = '/api/v1/campaigns/make-call';
    postData = {
        "reference_number":$(this).attr('reference'),
        "campaign_id":$(this).attr('campaign-id'),
        "lead_id":$(this).attr('lead-id'),
        "lead_data":[{
            "field_name":'Phone No',
            "field_value":$(this).attr('reference')
        }]
    }
    postToAPI(url, postData, 'POST', 'doNothing');
});
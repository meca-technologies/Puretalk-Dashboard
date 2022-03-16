
var leadsCampaign = new Vue({
    delimiters: ['[[', ']]'],
    el: '#leads-body',
    data: {
        leads:[]
    }
})

var leadsTable;


$('body').on('change','.lead-campaigns', function(){
    document.getElementById("lead-list-table-loading").style.display = '';
    document.getElementById("lead-table").style.display = 'none';
    var url = '/api/v1/leads?campaignid='+$(this).val()+'&skip='+String(0)+'&limit='+String(100000000);
    getLeadsCampaign(url);
});

function getLeadsCampaign(url){
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        leadsCampaign.leads = data;
        document.getElementById("lead-list-table-loading").style.display = 'none';
        document.getElementById("lead-table").style.display = '';
    });
}

$('#export-history').click(function(){
    var url = '/api/v1/leads/export?campaignid='+$("#campaign-body").val();
    var csv = '';
    var jqxhr = $.get( url, function(data) {
        console.log(data.length);
        for(var i = 0; i<data.length; i++){
            for(var j = 0; j<data[i].length; j++){
                data[i][j] = data[i][j].split('"').join("");
                data[i][j] = data[i][j].split("'").join("");
                data[i][j] = data[i][j].split("#").join("");
            }
            csv += data[i].join(',');
            csv += "\n";
        }
        //data.forEach(function(row) {
        //    csv += row.join(',');
        //    csv += "\n";
        //});
        console.log(csv);
        var hiddenElement = document.createElement('a');
        hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
        hiddenElement.target = '_blank';
        hiddenElement.download = 'leads.csv';
        hiddenElement.click();
    })
});

$("#recycle-leads-btn").click(function(){
    var dispo_classes = document.getElementsByClassName("dispo-check");
    var dispos = [];
    for(var i = 0; i<dispo_classes.length; i++){
        if(dispo_classes[i].checked){
            dispos.push($(dispo_classes[i]).attr('dispo'));
        }
    }
    var post_data = {
        'campaign_id':$("#campaign-body").val(),
        'dispos':dispos
    }
    console.log(post_data);
    var url = '/api/v1/leads/recycle';
    postToAPI(url, post_data, 'POST', 'doNothing');
});

$('body').on('change','.lead-campaigns-dnc', function(){
    var url = '/api/v1/leads?campaignid=' + $(this).val() + '&skip=0&limit=100&dnc=1';
    if($(this).val() == 'all'){
        var url = '/api/v1/leads?skip=0&limit=100&dnc=1';
    }
    try{
        leadsTable.destroy()
    }catch(error){}
    document.getElementById("lead-list-table-loading").style.display = '';
    document.getElementById("lead-table").style.display = 'none';
    document.getElementById("campaign-body-dnc").style.display = 'none';
    console.log(url);
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        leadsCampaign.leads = data;
        setTimeout(function(){
            leadsTable = $('#dnc-table').DataTable({
                "language": {
                  "paginate": {
                    "previous": "<<",
                    "next": ">>"
                  }
                }
            });
            document.getElementById("lead-list-table-loading").style.display = 'none';
            document.getElementById("lead-table").style.display = '';
            document.getElementById("campaign-body-dnc").style.display = '';
        }, 1000)
    })
})
var leadListTable;
try{
    document.getElementById("lead-list-table-loading").style.display = 'none'
}catch(error){}

var lead_items = new Vue({
    delimiters: ['[[', ']]'],
    el: '#lead-list-table',
    data: {
        lead_items:[]
    }
})

var lead_details = new Vue({
    delimiters: ['[[', ']]'],
    el: '#lead-item-details',
    data: {
        details:[],
        recordings:[]
    }
})

$('body').on('change','#list-body', function(){
    try{
        leadListTable.destroy()
    }catch(error){}
    console.log($(this).val());
    if($(this).val() != ''){
        try{
            $("#lead-list-table").fadeOut();
            $("#lead-list-table").promise().done(function(){
                $("#lead-list-table-loading").fadeIn();
            });
        }catch(error){}
        var url = '/api/vici/leads?list_id='+$(this).val();
        var jqxhr = $.get( url, function(data) {
            console.log(data);
            lead_items.lead_items = data['data'];
        }).always(function(){
            setTimeout(function(){
                try{
                    leadListTable = document.getElementById("lead-list-table");
                    console.log(leadListTable.nodeName);
                    if(leadListTable.nodeName == 'TABLE'){
                        leadListTable = $('#lead-list-table').DataTable({
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
                    }
                }catch(error){}
                try{
                    $("#lead-list-table-loading").fadeOut();
                    $("#lead-list-table-loading").promise().done(function(){
                        $("#lead-list-table").fadeIn();
                    });
                }catch(error){}
            },1000)
        });
    }
})

$('body').on('click','.lead-edit', function(){
    try{
        document.getElementById('lead-details-edit-loading').style.display = '';
        document.getElementById('lead-details-edit').style.display = 'none';
    }catch(error){}
    lead_index = $(this).attr('lead-id');
    lead_details.details = lead_items.lead_items[lead_index];

    lead_id = lead_details.details['lead_id'];
    console.log(lead_id);
    var url = '/api/vici/recordings?lead_id='+lead_id;
    console.log(url);
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        lead_details.recordings = data['data'];
        try{
            document.getElementById('lead-details-edit-loading').style.display = 'none';
            document.getElementById('lead-details-edit').style.display = '';
        }catch(error){}
    })
});
var summary = new Vue({
    delimiters: ['[[', ']]'],
    el: '#company-lead-summary',
    data: {
        summary:{
            'campaign_count':0,
            'total_calls':0,
            'total_calls_made':0,
            'total_calls_xfer':0,
            'total_call_time':0
        }
    }
})

var dispo_summary = new Vue({
    delimiters: ['[[', ']]'],
    el: '#dispo-body',
    data: {
        'dispositions':[
            {
                'status':'',
                'count':0
            }
        ]
    }
})

var interest_summary = new Vue({
    delimiters: ['[[', ']]'],
    el: '#campaign-breakdown',
    data: {
        'interests':[
            {
                "campaign_id": "", 
                "interested": 0, 
                "total": 0
            }
        ]
    }
})

var billing_summary = new Vue({
    delimiters: ['[[', ']]'],
    el: '#campaign-billing-breakdown',
    data: {
        'campaign_minute_breakdown': [
            {
                "campaign_id": "", 
                "rounded_minutes": 0, 
                "total_charge": 0
            }
        ]
    }
})

var dispo_table;
var campaign_breakdown_table;
var cost_breakdown_table;

function updateSummary(formatted_from, formatted_to='2031-11-30'){
    try{
        dispo_table.destroy()
    }catch(error){}
    try{
        campaign_breakdown_table.destroy()
    }catch(error){}
    try{
        cost_breakdown_table.destroy()
    }catch(error){}

    var url = '/api/vici/call_summary?limit=100000&offset=0';

    url += '&from='+formatted_from+' 00:00:00&to='+formatted_to+' 23:59:59';
    var jqxhr = $.get(url, function(data) {
        summary.summary['total_calls'] = data['data']['total_calls'];
        summary.summary['total_calls_made'] = data['data']['total_calls_made'];
        summary.summary['total_calls_xfer'] = data['data']['total_calls_xfer'];
        summary.summary['total_call_time'] = data['data']['total_call_time'];

        dispo_summary['dispositions'] = data['data']['statuses'];

        interest_summary['interests'] = data['data']['interest_breakdown'];
        billing_summary['campaign_minute_breakdown'] = data['data']['billing']['campaign_minute_breakdown'];
    }).always(function(){
        $("#company-lead-summary-loading").fadeOut();
        $("#company-lead-summary-loading").promise().done(function(){
            $("#company-lead-summary").fadeIn();
        });
        try{
            $("#dispo-body-loading").fadeOut();
            $("#dispo-body-loading").promise().done(function(){
                $("#dispo-body").fadeIn();
            });
        }catch(error){}
        try{
            $("#campaign-breakdown-loading").fadeOut();
            $("#campaign-breakdown-loading").promise().done(function(){
                $("#campaign-breakdown").fadeIn();
            });
            setTimeout(function(){
                calculateProgressBars();
            },100)
        }catch(error){}
        try{
            $("#campaign-billing-breakdown-loading").fadeOut();
            $("#campaign-billing-breakdown-loading").promise().done(function(){
                $("#campaign-billing-breakdown").fadeIn();
            });
        }catch(error){}

        // CREATE DATATABLES *******************************************************************
        setTimeout(function(){
            // DISPOSITION TABLE ***********************************************************
            try{
                dispo_table = document.getElementById("dispo-body");
                console.log(dispo_table.nodeName);
                if(dispo_table.nodeName == 'TABLE'){
                    dispo_table = $('#dispo-body').DataTable({
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
            // INTEREST TABLE ***********************************************************
            try{
                campaign_breakdown_table = document.getElementById("campaign-breakdown");
                console.log(campaign_breakdown_table.nodeName);
                if(campaign_breakdown_table.nodeName == 'TABLE'){
                    campaign_breakdown_table = $('#campaign-breakdown').DataTable({
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
            // COST BREAKDOWN TABLE ***********************************************************
            try{
                cost_breakdown_table = document.getElementById("campaign-billing-breakdown");
                console.log(cost_breakdown_table.nodeName);
                if(cost_breakdown_table.nodeName == 'TABLE'){
                    cost_breakdown_table = $('#campaign-billing-breakdown').DataTable({
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
        },2000)
    });
    var jqxhr = $.get( '/api/vici/campaigns?source=test&stage=csv', function(data) {
        summary.summary['campaign_count'] = data['data'].length;
    })
}
var campaignCostBreakdownReport = new Vue({
    delimiters: ['[[', ']]'],
    el: '#cost-breakdown-report',
    data: {
        costBreakdown:[]
    }
})

var cost_breakdown_table;
try{
    var costBreakdownTable = document.getElementById("cost-breakdown-report");
    console.log(costBreakdownTable.nodeName);
    if(costBreakdownTable.nodeName == 'TABLE'){
        cost_breakdown_table = $('#cost-breakdown-report').DataTable({
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

$("#campaign-filter-report").click(function(){
    if(validateForm(['#campaign-body', '#from-date', '#to-date'])){
        document.getElementById("cost-breakdown-report-loading").style.display = '';
        document.getElementById("cost-breakdown-report").style.display = 'none';
        var url = '/api/v1/wallet/earnings/company?campaignid='+$("#campaign-body").val()+'&from='+$("#from-date").val()+'&to='+$("#to-date").val();
        var jqxhr = $.get( url, function(data) {
            console.log(data);
            campaignCostBreakdownReport.costBreakdown = data;
            try{
                cost_breakdown_table.destroy();
            }catch(error){}
        }).always(function(){
            setTimeout(function(){
                costBreakdownTable = document.getElementById("cost-breakdown-report");
                console.log(costBreakdownTable.nodeName);
                if(costBreakdownTable.nodeName == 'TABLE'){
                    cost_breakdown_table = $('#cost-breakdown-report').DataTable({
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
                document.getElementById("cost-breakdown-report-loading").style.display = 'none';
                document.getElementById("cost-breakdown-report").style.display = '';
            }, 1000)
        });
    }
});
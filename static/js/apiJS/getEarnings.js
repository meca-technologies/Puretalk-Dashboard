var dataStr = '';
var salesChart = null;
getBuiltInDates('month');
document.getElementById('fromDate').value = getBuiltInDates('month');
document.getElementById('toDate').value = getBuiltInDates('month');
function updateChart(type){
    fromDate = document.getElementById('fromDate').value;
    toDate = document.getElementById('toDate').value;

    var url = '/api/v1/wallet/earnings?from='+fromDate+'&to='+toDate;
    console.log(url);
    var jqxhr = $.get( url, function(data) {
        var labels = [];
        var counts = [];
        for(var i = 0; i<data.length; i++){
            labels.push(data[i]['entry_date']);
            counts.push(data[i]['paid_balance']);
        }
        if(dataStr == JSON.stringify(data)){
            return;
        }
        else{
            dataStr = JSON.stringify(data);
        }
        var $chart = $('#chart-revenue-dark-new');
        try{
            salesChart.destroy();
        }catch(error){}
        salesChart = new Chart($chart, {
            type: 'line',
            options: {
                scales: {
                    yAxes: [{
                        gridLines: {
                            color: Charts.colors.gray[700],
                            zeroLineColor: Charts.colors.gray[700]
                        },
                        ticks: {

                        }
                    }]
                },
                tooltipTemplate: "value",
            },
            tooltips: {
                callbacks: {
                    label: function(item, data) {
                        var label = data.datasets[item.datasetIndex].label || '';
                        var yLabel = item.yLabel;
                        var content = '';
            
                        if (data.datasets.length > 1) {
                            content += '<span class="popover-body-label mr-auto">' + label + '</span>';
                        }
        
                        content += '$' + formatMoney(yLabel) + '';
                        return content;
                    }
                }
            },
            data: {
                labels: labels,
                datasets: [{
                    label: 'Balance',
                    data: counts
                }]
            }
        });
    });
}

function getBuiltInDates(type){
    var d = new Date();
    console.log(type);
    if(type == 'month'){
        var currMonth = addZero(d.getMonth()+1);
        var currDay = addZero(d.getDate());
        var currYear = (d.getFullYear());

        document.getElementById('fromDate').value = currYear + '-' + currMonth + '-' + '01';
        document.getElementById('toDate').value = currYear + '-' + currMonth + '-' + currDay;
        updateChart();
    }
    else if(type == 'week'){
        var currMonth = addZero(d.getMonth()+1);
        var currDay = addZero(d.getDate());
        var currYear = d.getFullYear();

        var newD = new Date();
        newD.setDate(newD.getDate()-7);
        var newMonth = addZero(newD.getMonth()+1);
        var newDay = addZero(newD.getDate());
        var newYear = newD.getFullYear();

        document.getElementById('fromDate').value = newYear + '-' + newMonth + '-' + newDay;
        document.getElementById('toDate').value = currYear + '-' + currMonth + '-' + currDay;
        updateChart();
    }
}
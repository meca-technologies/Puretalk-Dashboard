var chart;
var dataStr = '';
var salesChart = null;
//document.getElementById('fromdate').value = '2021-08-31';
//document.getElementById('todate').value = '2022-10-31';

var last_data = null;

function updateChart(){
    fromDate = document.getElementById('fromdate').value;
    toDate = document.getElementById('todate').value;

    //var url = '/api/v1/leads/counts?from='+fromDate+'&to='+toDate;
    var url = '/api/vici/call_by_date?from='+fromDate+'&to='+toDate+'&limit=100000&offset=0'
    console.log(url);
    var jqxhr = $.get( url, function(data) {
        var formatted_data = data;
        if(formatted_data.length<1){
            formatted_data.push({
                "count": 0,
                "full_date": fromDate
            })
            formatted_data.push({
                "count": 0, 
                "full_date": toDate
            })
        }
        if(last_data == null){
            chart.data = formatted_data;
            last_data = formatted_data;
        }
        else if(formatted_data.length != last_data.length || formatted_data[formatted_data.length-1]['count'] != last_data[last_data.length-1]['count']){
            chart.data = formatted_data;
            last_data = formatted_data;
        }
    })
    .fail(function() {
        data = []
        data.push({
            "count": 0, 
            "full_date": fromDate
        })
        data.push({
            "count": 0, 
            "full_date": toDate
        })
        chart.data = data;
    });
}

function getBuiltInDates(type){
    var d = new Date();
    if(type == 'month'){
        var currMonth = addZero(d.getMonth()+1);
        var currDay = addZero(d.getDate());
        var currYear = (d.getFullYear());

        document.getElementById('fromdate').value = currYear + '-' + currMonth + '-' + '01';
        document.getElementById('todate').value = currYear + '-' + currMonth + '-' + currDay;
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

        document.getElementById('fromdate').value = newYear + '-' + newMonth + '-' + newDay;
        document.getElementById('todate').value = currYear + '-' + currMonth + '-' + currDay;
        updateChart();
    }
}

getBuiltInDates('month')

am4core.ready(function() {

    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end
    am4core.options.autoSetClassName = true;
    // Create chart instance
    chart = am4core.create("chartdiv", am4charts.XYChart);

    // Set input format for the dates
    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd";

    // Create axes
    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.min = 0;

    // Create series
    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.valueY = "count";
    series.dataFields.dateX = "full_date";
    series.tooltipText = "{count} Calls"
    series.tensionX = 0.9;
    series.strokeWidth = 3;
    series.strokeWidth = 2;
    series.minBulletDistance = 15;
    series.stroke = am4core.color("#5e72e4");
    series.fill = am4core.color("#5e72e4");
    series.fillOpacity = 1;
    var gradient = new am4core.LinearGradient();
    gradient.addColor(am4core.color("#5e72e4"), 0.2);
    gradient.addColor(am4core.color("#5e72e4"), 0);
    gradient.rotation = 90;
    series.fill = gradient;

    // Drop-shaped tooltips
    series.tooltip.background.cornerRadius = 20;
    series.tooltip.background.strokeOpacity = 0;
    series.tooltip.pointerOrientation = "vertical";
    series.tooltip.label.minWidth = 10;
    series.tooltip.label.minHeight = 10;
    series.tooltip.label.textAlign = "middle";
    series.tooltip.label.textValign = "middle";

    // Make bullets grow on hover
    var bullet = series.bullets.push(new am4charts.CircleBullet());
    bullet.circle.strokeWidth = 2;
    bullet.circle.radius = 4;
    bullet.circle.fill = am4core.color("#fff");

    var bullethover = bullet.states.create("hover");
    bullethover.properties.scale = 1.3;

    // Make a panning cursor
    chart.cursor = new am4charts.XYCursor();
    chart.cursor.behavior = "panXY";
    chart.cursor.xAxis = dateAxis;
    chart.cursor.snapToSeries = series;

    // Create vertical scrollbar and place it before the value axis
    chart.scrollbarY = new am4core.Scrollbar();
    chart.scrollbarY.parent = chart.leftAxesContainer;
    chart.scrollbarY.toBack();

    // Create a horizontal scrollbar with previe and place it underneath the date axis
    chart.scrollbarX = new am4charts.XYChartScrollbar();
    chart.scrollbarX.series.push(series);
    chart.scrollbarX.parent = chart.bottomAxesContainer;

    dateAxis.start = 0;
    dateAxis.keepSelection = true;


}); // end am4core.ready()

updateChart();
setTimeout(function(){
    updateChart();
}, 10000)
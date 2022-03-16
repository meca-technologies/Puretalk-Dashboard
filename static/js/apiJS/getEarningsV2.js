var dataStr = '';
var salesChart = null;
getBuiltInDates('month');

function updateChart(){
    fromDate = document.getElementById('fromDate').value;
    toDate = document.getElementById('toDate').value;

    var url = '/api/v1/wallet/earnings_new?from='+fromDate+'&to='+toDate;
    console.log(url);
    var jqxhr = $.get( url, function(data) {
        if(data.length<1){
            data.push({
                "paid_balance": 0, 
                "entry_date": fromDate
            })
            data.push({
                "paid_balance": 0, 
                "full_date": toDate
            })
        }
        console.log(data);
        chart.data = data;
    })
    .fail(function() {
        data = []
        data.push({
            "charge_amount": 0, 
            "entry_date": fromDate
        })
        data.push({
            "charge_amount": 0, 
            "full_date": toDate
        })
        chart.data = data;
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
        var currDay = addZero(d.getDate()-1);
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
    series.dataFields.valueY = "charge_amount";
    series.dataFields.dateX = "entry_date";
    series.tooltipText = "${charge_amount}"
    series.tensionX = .9;
    series.strokeWidth = 3;
    series.strokeWidth = 2;
    series.minBulletDistance = 15;
    series.stroke = am4core.color("#5e72e4");
    series.fill = am4core.color("#5e72e4");

    // Drop-shaped tooltips
    series.tooltip.background.cornerRadius = 20;
    series.tooltip.background.strokeOpacity = 0;
    series.tooltip.pointerOrientation = "vertical";
    series.tooltip.label.minWidth = 40;
    series.tooltip.label.minHeight = 40;
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

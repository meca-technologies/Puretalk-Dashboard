var first_run = true;
am4core.ready(function() {

    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end

    var chart = am4core.create("chartdiv-live", am4charts.XYChart);
    chart.hiddenState.properties.opacity = 0;

    chart.padding(0, 0, 0, 0);

    chart.zoomOutButton.disabled = true;

    var data = [];
    var visits = 10;
    var i = 0;

    for (i = 0; i <= 100; i++) {
        visits = 0;
        data.push({
            date: new Date().setSeconds(i - 30),
            value: visits
        });
    }

    chart.data = data;

    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.grid.template.location = 0;
    dateAxis.renderer.minGridDistance = 30;
    dateAxis.dateFormats.setKey("second", "ss");
    dateAxis.periodChangeDateFormats.setKey("second", "[bold]h:mm a");
    dateAxis.periodChangeDateFormats.setKey("minute", "[bold]h:mm a");
    dateAxis.periodChangeDateFormats.setKey("hour", "[bold]h:mm a");
    dateAxis.renderer.inside = true;
    dateAxis.renderer.axisFills.template.disabled = true;
    dateAxis.renderer.ticks.template.disabled = true;

    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;
    valueAxis.interpolationDuration = 500;
    valueAxis.rangeChangeDuration = 500;
    valueAxis.renderer.inside = true;
    valueAxis.renderer.minLabelPosition = 0.05;
    valueAxis.renderer.maxLabelPosition = 0.95;
    valueAxis.renderer.axisFills.template.disabled = true;
    valueAxis.renderer.ticks.template.disabled = true;

    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.dateX = "date";
    series.dataFields.valueY = "value";
    series.interpolationDuration = 500;
    series.defaultState.transitionDuration = 0;
    series.tensionX = 0.8;
    series.stroke = am4core.color("#5e72e4");
    series.fill = am4core.color("#5e72e4");

    chart.events.on("datavalidated", function() {
        dateAxis.zoom({
            start: 1 / 15,
            end: 1.2
        }, false, true);
    });

    dateAxis.interpolationDuration = 500;
    dateAxis.rangeChangeDuration = 500;

    document.addEventListener("visibilitychange", function() {
        if (document.hidden) {
            if (interval) {
                clearInterval(interval);
            }
        } else {
            startInterval();
        }
    }, false);

    // add data
    var interval;

    function startInterval() {
        //interval = setInterval(function() {
            var url = '/api/vici/call_summary?limit=100000&offset=0';
            var d = new Date();
            var formatted_today = formatDate(d);
            url +='&from='+formatted_today+'%2000:00:00&to=2031-10-31%2023:59:59&'
            var jqxhr = $.get( url, function(data) {
                var formatted_data = data["data"]["calls_by_date"];
                if(first_run){
                    var starter_data = [];
                    for (var i = 0; i <= 100; i++) {
                        visits = formatted_data[0]['count'];
                        starter_data.push({
                            date: new Date().setSeconds(i - 30),
                            value: visits
                        });
                    }
                    chart.data = starter_data;
                    first_run = false;
                }
                var lastdataItem = series.dataItems.getIndex(series.dataItems.length - 1);
                chart.addData({
                        date: new Date(lastdataItem.dateX.getTime() + 5000),
                        value: formatted_data[0]['count']
                    },
                    1
                );
            })
        //}, 5000);
    }

    startInterval();

    // all the below is optional, makes some fancy effects
    // gradient fill of the series
    series.fillOpacity = 1;
    var gradient = new am4core.LinearGradient();
    gradient.addColor(am4core.color("#5e72e4"), 0.2);
    gradient.addColor(am4core.color("#5e72e4"), 0);
    series.fill = gradient;

    // this makes date axis labels to fade out
    dateAxis.renderer.labels.template.adapter.add("fillOpacity", function(fillOpacity, target) {
        var dataItem = target.dataItem;
        return dataItem.position;
    })

    // need to set this, otherwise fillOpacity is not changed and not set
    dateAxis.events.on("validated", function() {
        am4core.iter.each(dateAxis.renderer.labels.iterator(), function(label) {
            valueAxis.min = 0;
            valueAxis.extraMax = 0.3;             
            label.fillOpacity = label.fillOpacity;
        })
    })

    // this makes date axis labels which are at equal minutes to be rotated
    dateAxis.renderer.labels.template.adapter.add("rotation", function(rotation, target) {
        var dataItem = target.dataItem;
        if (dataItem.date && dataItem.date.getTime() == am4core.time.round(new Date(dataItem.date.getTime()), "minute").getTime()) {
            target.verticalCenter = "middle";
            target.horizontalCenter = "left";
            return -90;
        } else {
            target.verticalCenter = "bottom";
            target.horizontalCenter = "middle";
            return 0;
        }
    })

    // bullet at the front of the line
    var bullet = series.createChild(am4charts.CircleBullet);
    bullet.circle.radius = 5;
    bullet.fillOpacity = 1;
    bullet.fill = chart.colors.getIndex(0);
    bullet.isMeasured = false;

    series.events.on("validated", function() {
        bullet.moveTo(series.dataItems.last.point);
        bullet.validatePosition();
    });

}); // end am4core.ready()
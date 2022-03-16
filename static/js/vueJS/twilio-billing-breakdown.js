var twilioBillingSummary = new Vue({
    delimiters: ['[[', ']]'],
    el: '#twilio-summary-billing',
    data: {
        "companies":{},
        "total_cost":0,
        "puretalk_companies":{}
    }
})
var twilioBillingLoading = new Vue({
    delimiters: ['[[', ']]'],
    el: '#twilio-summary-billing-loading',
    data: {
        "current":0,
        "max":0
    }
})

var chartOne;
var chartTwo;
var company_data = [];
var cost_data = [];

var company_list = [];
var count_company = 0;
$("#twilio-filter").click(function(){
    count_company = 0;
    var url = '/api/v1/companies';
    company_list = [];
    twilioBillingLoading.current = count_company;
    
    document.getElementById("twilio-summary-billing-loading").style.display = '';
    document.getElementById("twilio-summary-body").style.display = 'none';
    document.getElementById("twilio-summary-filters").style.display = 'none';
    
    var company_value = $("#twilio-company-select").val();
    if(company_value == 'all'){
        var jqxhr = $.get( url, function(data) {
            for(var i = 0; i<data.length; i++){
                company_list.push(data[i]['id']);
            }
            twilioBillingLoading.max = company_list.length;
        }).always(function(){
            getUsage(company_list);
        });
    }
    else{
        company_list.push(company_value);
        twilioBillingLoading.max = 1;
        getUsage(company_list);
    }
});

function getUsage(company_list){
    var company_dict = {};
    cost_data = [];
    company_data = [];
    puretalk_companies_data = {};
    total_cost = 0;
    for(var i = 0; i<company_list.length; i++){
        var url = '/api/v1/twilio/usage?companyid='+company_list[i]+'&type='+$("#twilio-summary-select").val();
        console.log(url);
        var jqxhr = $.get( url, function(data) {
            var company_keys = Object.keys(data['company_breakdown']);
            for(var i = 0; i<company_keys.length; i++){
                company_data.push({
                    'company_name':data['company_breakdown'][company_keys[i]]['company_name'],
                    'total_cost':formatMoney(data['company_breakdown'][company_keys[i]]['total_cost'])
                });
                console.log(parseFloat(data['company_breakdown'][company_keys[i]]['total_cost']));
                total_cost += parseFloat(data['company_breakdown'][company_keys[i]]['total_cost']);
            }
            
            var cost_keys = Object.keys(data['cost_breakdown']);
            for(var i = 0; i<cost_keys.length; i++){
                if(cost_data.length > 0){
                    var found = false;
                    for(var j = 0; j<cost_data.length; j++){
                        if(cost_keys[i] == cost_data[j]['cost_name']){
                            cost_data[j]['total_cost'] += parseFloat(data['cost_breakdown'][cost_keys[i]]);
                            found = true;
                        }
                    }
                    if(found == false){
                        cost_data.push({
                            'cost_name':cost_keys[i],
                            'total_cost':parseFloat(data['cost_breakdown'][cost_keys[i]])
                        })
                    }
                }
                else{
                    cost_data.push({
                        'cost_name':cost_keys[i],
                        'total_cost':parseFloat(data['cost_breakdown'][cost_keys[i]])
                    })
                }
            }
            var company_id = Object.keys(data['company_summary_breakdown'])
            if(company_id[0] !== undefined){
                company_dict[company_id[0]] = data['company_summary_breakdown'][company_id[0]];
            }
            twilioBillingLoading.current = count_company;
            count_company+=1;
        });
        var url = '/api/v1/leads/time_summary?companyid='+company_list[i];
        var jqxhr = $.get( url, function(data) {
            puretalk_companies_data[data['company_id']] = {
                'company_id':data['company_id'],
                'minutes':data['total_time_rounded_taken'],
                'charge':data['total_charge']
            };
        })
    }
    console.log(company_dict);
    var checkMe = setInterval(function(){
        if(count_company >= company_list.length){
            console.log('done counting');
            twilioBillingSummary.companies = company_dict;
            twilioBillingSummary.total_cost = total_cost;
            twilioBillingSummary.puretalk_companies = puretalk_companies_data;
            console.log(puretalk_companies_data);
            document.getElementById("twilio-summary-billing-loading").style.display = 'none';
            document.getElementById("twilio-summary-body").style.display = '';
            document.getElementById("twilio-summary-filters").style.display = '';
            clearInterval(checkMe);
        }
    }, 1000)
}

updateCompanyCostBreakdown([]);
updateCostBreakdown([]);

function updateCompanyCostBreakdown(_data){
    am5.ready(function() {
        
        // Create chartOne element
        // https://www.amcharts.com/docs/v5/getting-started/#Root_element
        chartOne = am5.Root.new("chartdiv");
        
        
        // Set themes
        // https://www.amcharts.com/docs/v5/concepts/themes/
        chartOne.setThemes([
        am5themes_Animated.new(chartOne)
        ]);
        
        
        // Create chart
        // https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/
        var chart = chartOne.container.children.push(am5percent.PieChart.new(chartOne, {
        layout: chartOne.verticalLayout,
        innerRadius: am5.percent(50)
        }));
        
        
        // Create series
        // https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/#Series
        var series = chart.series.push(
            am5percent.PieSeries.new(chartOne, {
                valueField: "total_cost",
                categoryField: "company_name",
                alignLabels: false
            })
        );

        // Disabling labels and ticks
        series.labels.template.set("visible", false);
        series.ticks.template.set("visible", false);
        
        // Set data
        // https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/#Setting_data
        series.data.setAll(_data);

        // Configuring slices
        series.slices.template.setAll({
        stroke: am5.color(0xffffff),
        strokeWidth: 2
        })
        
        
        // Create legend
        // https://www.amcharts.com/docs/v5/charts/percent-charts/legend-percent-series/
        var legend = chart.children.push(am5.Legend.new(chartOne, {
        centerX: am5.percent(50),
        x: am5.percent(50),
        marginTop: 15,
        marginBottom: 15,
        }));
        
        legend.data.setAll(series.dataItems);
        
        
        // Play initial series animation
        // https://www.amcharts.com/docs/v5/concepts/animations/#Animation_of_series
        series.appear(1000, 100);
        
        $("#twilio-summary-filters").change(function(){
            console.log('TESTING');
        })

        setInterval(function() {
            series.data.setAll(company_data);
            legend.data.setAll(series.dataItems);
          }, 2000);
        
    }); // end am5.ready()
}

function updateCostBreakdown(_data){
    am5.ready(function() {
        
        // Create chartTwo element
        // https://www.amcharts.com/docs/v5/getting-started/#Root_element
        chartTwo = am5.Root.new("chartdiv2");
        
        
        // Set themes
        // https://www.amcharts.com/docs/v5/concepts/themes/
        chartTwo.setThemes([
        am5themes_Animated.new(chartTwo)
        ]);
        
        
        // Create chart
        // https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/
        var chart = chartTwo.container.children.push(am5percent.PieChart.new(chartTwo, {
        layout: chartTwo.verticalLayout,
        innerRadius: am5.percent(50)
        }));
        
        
        // Create series
        // https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/#Series
        var series = chart.series.push(
            am5percent.PieSeries.new(chartTwo, {
                valueField: "total_cost",
                categoryField: "cost_name",
                alignLabels: false
            })
        );

        // Disabling labels and ticks
        series.labels.template.set("visible", false);
        series.ticks.template.set("visible", false);
        
        // Set data
        // https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/#Setting_data
        series.data.setAll(_data);

        // Configuring slices
        series.slices.template.setAll({
        stroke: am5.color(0xffffff),
        strokeWidth: 2
        })
        
        
        // Create legend
        // https://www.amcharts.com/docs/v5/charts/percent-charts/legend-percent-series/
        var legend = chart.children.push(am5.Legend.new(chartTwo, {
        centerX: am5.percent(50),
        x: am5.percent(50),
        marginTop: 15,
        marginBottom: 15,
        }));
        
        legend.data.setAll(series.dataItems);
        
        
        // Play initial series animation
        // https://www.amcharts.com/docs/v5/concepts/animations/#Animation_of_series
        series.appear(1000, 100);

        setInterval(function() {
            series.data.setAll(cost_data);
            legend.data.setAll(series.dataItems);
          }, 2000);
        
    }); // end am5.ready()
}
function updateChart(){var r=_0x3c5aff;fromDate=document[r(223)]("fromdate")[r(194)],toDate=document.getElementById(r(244)).value;var t=r(230)+fromDate+r(178)+toDate;console[r(235)](t),$.get(t,function(t){var a=r;if(t[a(196)]<1)t[a(185)]({company_id:"",count:0,date:formatDate(fromDate),full_date:fromDate}),t[a(185)]({company_id:"",count:0,date:formatDate(toDate),full_date:toDate});else for(var e=0;e<t[a(196)];e++)t[e].full_date=formatDate(t[e][a(172)]);chart[a(245)]=t}).fail(function(){var t=r;data=[],data.push({company_id:"",count:0,date:formatDate(fromDate),full_date:fromDate}),data[t(185)]({company_id:"",count:0,date:formatDate(toDate),full_date:toDate}),chart.data=data})}function _0xb1c3(t,a){var e=_0x1a65();return(_0xb1c3=function(t,a){return e[t-=170]})(t,a)}function _0x1a65(){var t=["value","minHeight","length","15rrLnyu","middle","2021-08-31","useTheme","chartdiv","DateAxis","snapToSeries","Scrollbar","stroke","1206486PyHzVv","1317619TnKygQ","circle","minWidth","inputDateFormat","minBulletDistance","getMonth","scale","XYChart","2569824xWfqCE","parent","dateX","fromdate","strokeOpacity","pointerOrientation","getDate","label","getElementById","cursor","textValign","{count} Calls","textAlign","leftAxesContainer","bottomAxesContainer","/api/v1/leads/counts?from=","1794162EjcGOk","valueY","ValueAxis","#fff","log","create","tensionX","vertical","getFullYear","2973168fjuFQW","tooltip","#5e72e4","3205853ZfRegp","todate","data","LineSeries","ready","full_date","month","date","panXY","xAxes","scrollbarY","2711972OMaQqz","CircleBullet","&to=","99YMCXgk","fill","keepSelection","series","background","xAxis","push","strokeWidth","toBack","autoSetClassName","scrollbarX","yyyy-MM-dd","color","yAxes","cornerRadius"];return(_0x1a65=function(){return t})()}function getBuiltInDates(t){var a,e,r,o,c=_0x3c5aff,n=new Date;"month"==t?(a=addZero(n[c(212)]()+1),e=addZero(n[c(221)]()),r=n[c(239)](),document[c(223)]("fromdate")[c(194)]=r+"-"+a+"-01",document[c(223)](c(244)).value=r+"-"+a+"-"+e,updateChart()):"week"==t&&(a=addZero(n.getMonth()+1),e=addZero(n[c(221)]()),r=n[c(239)](),(o=new Date).setDate(o[c(221)]()-7),t=addZero(o[c(212)]()+1),n=addZero(o.getDate()),o=o[c(239)](),document.getElementById(c(218))[c(194)]=o+"-"+t+"-"+n,document[c(223)](c(244))[c(194)]=r+"-"+a+"-"+e,updateChart())}var _0x3c5aff=_0xb1c3;!function(){for(var t=_0xb1c3,a=_0x1a65();;)try{if(724653==+parseInt(t(207))+parseInt(t(176))/2+parseInt(t(206))/3+parseInt(t(240))/4+parseInt(t(197))/5*(parseInt(t(231))/6)+-parseInt(t(243))/7+parseInt(t(215))/8*(-parseInt(t(179))/9))break;a.push(a.shift())}catch(t){a.push(a.shift())}}();var chart,dataStr="",salesChart=null;getBuiltInDates(_0x3c5aff(171)),document[_0x3c5aff(223)](_0x3c5aff(218))[_0x3c5aff(194)]=_0x3c5aff(199),document.getElementById(_0x3c5aff(244))[_0x3c5aff(194)]="2021-09-04",updateChart(),am4core[_0x3c5aff(247)](function(){var t=_0x3c5aff;am4core[t(200)](am4themes_animated),am4core.options[t(188)]=!0,(chart=am4core[t(236)](t(201),am4charts[t(214)])).dateFormatter[t(210)]=t(190);var a=chart[t(174)][t(185)](new am4charts[t(202)]);chart[t(192)][t(185)](new am4charts[t(233)]).min=0;var e=chart.series[t(185)](new am4charts[t(246)]);e.dataFields[t(232)]="count",e.dataFields[t(217)]=t(170),e.tooltipText=t(226),e[t(237)]=.8,e[t(186)]=3,e[t(186)]=2,e[t(211)]=15,e[t(205)]=am4core[t(191)](t(242)),e.fill=am4core[t(191)](t(242)),e[t(241)][t(183)][t(193)]=20,e[t(241)][t(183)][t(219)]=0,e[t(241)][t(220)]=t(238),e.tooltip.label[t(209)]=40,e[t(241)][t(222)][t(195)]=40,e.tooltip[t(222)][t(227)]=t(198),e[t(241)].label[t(225)]=t(198);var r=e.bullets[t(185)](new am4charts[t(177)]);r[t(208)][t(186)]=2,r[t(208)].radius=4,r[t(208)][t(180)]=am4core[t(191)](t(234)),r.states.create("hover").properties[t(213)]=1.3,chart[t(224)]=new am4charts.XYCursor,chart.cursor.behavior=t(173),chart[t(224)][t(184)]=a,chart.cursor[t(203)]=e,chart[t(175)]=new am4core[t(204)],chart[t(175)].parent=chart[t(228)],chart.scrollbarY[t(187)](),chart.scrollbarX=new am4charts.XYChartScrollbar,chart[t(189)][t(182)].push(e),chart[t(189)][t(216)]=chart[t(229)],a.start=0,a[t(181)]=!0});
var summary = new Vue({
    delimiters: ['[[', ']]'],
    el: '#summary-stats',
    data: {
        summary:{}
    }
})

function updateSummary(){
    var jqxhr = $.get( '/api/v1/companies/summary', function(data) {
        summary.summary = data;
    }).always(function(){
        document.getElementById('summary-stats-loading').style.display = 'none';
        document.getElementById('summary-stats').style.display = '';
    });
}

updateSummary();
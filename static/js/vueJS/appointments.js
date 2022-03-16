document.getElementById('appointments-body-loading').style.display = '';
document.getElementById('appointments-body').style.display = 'none';

var appointments = new Vue({
    delimiters: ['[[', ']]'],
    el: '#appointments-body',
    data: {
        appointments:[],
        length:0
    }
})

function updateAppointments(){
    var jqxhr = $.get( '/api/v1/appointments?limit=2000', function(data) {
        console.log(data);
        appointments.appointments = data;
        appointments.length = data.length;
    }).always(function(){
        document.getElementById('appointments-body-loading').style.display = 'none';
        document.getElementById('appointments-body').style.display = '';
        setTimeout(function(){
            $('#appointments-body').DataTable({
                "language": {
                  "paginate": {
                    "previous": "<<",
                    "next": ">>"
                  }
                }
            });
        },1000)
    });
}

updateAppointments();
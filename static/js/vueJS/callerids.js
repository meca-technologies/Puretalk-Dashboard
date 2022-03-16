try{
    const inputElement = document.getElementById("import_file");
    inputElement.addEventListener("change", handleFiles, false);
}catch(error){}

var csvDataFull = [];
function handleFiles() {
    const myFile = this.files[0]; /* now you can work with the file list */
    var reader = new FileReader();
    var parseData = [];
    reader.addEventListener('load', function (e) {
        var csvdata = e.target.result; 
        var lineBreaks = csvdata.split('\n');
        csvDataFull = lineBreaks;
        console.log(csvDataFull);
    });
    reader.readAsBinaryString(myFile);
}

$('body').on('click','#importCSV', function(){
    document.getElementById("lead-import-loading").style.display = '';
    document.getElementById("lead-import-card").style.display = 'none';
    var campaignID = $('#campaign-body').val();
    var postData = [];

    for(var i = 0; i<csvDataFull.length; i++){
        try{
            postData.push({
                "caller_id":csvDataFull[i].split(',')[0].replace(/\D/g,''),
                "name":csvDataFull[i].split(',')[1].replace('\r','')
            })
        }catch(error){
            postData.push({
                "caller_id":csvDataFull[i].replace(/\D/g,'')
            })
        }
    }
    console.log(postData);
    postToAPI('/api/v1/campaigns/caller-ids', postData, 'POST', 'reloadPage');
})

var callerIDTable = $('#caller-id-table').DataTable({
                "language": {
                  "paginate": {
                    "previous": "<<",
                    "next": ">>"
                  }
                }
            });
var callerIDs = new Vue({
    delimiters: ['[[', ']]'],
    el: '#caller-id-body',
    data: {
        callerIDs:[]
    }
})

function updateCallerIDs(){
    var url = '/api/v1/campaigns/caller-ids';
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        callerIDs.callerIDs = data;
        try{
            callerIDTable.destroy()
        }catch(error){}
        setTimeout(function(){
            callerIDTable = $('#caller-id-table').DataTable({
                "language": {
                  "paginate": {
                    "previous": "<<",
                    "next": ">>"
                  }
                }
            });
        },1000)
    })
}
updateCallerIDs();
//$('body').on('change','#campaign-body', function(){
//    console.log('Campaign Changed')
//    if($(this).attr('trigger-type') == 'caller-id'){
//        if($(this).val() != ''){
//            updateCallerIDs();
//        }
//    }
//})


var callerIDCheck;
$('body').on('click','.verify-caller', function(){
    var payload = {
        "id":$(this).attr('caller-id')
    }
    url = '/api/v1/campaigns/caller-ids/verify';
    $.ajax({
        type: 'POST',
        url: url,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: JSON.stringify(payload),
        success: function(data){
            console.log("data");
            document.getElementById("verify-code").innerHTML = String(data['verification_code']).substring(0,3) + "-" + String(data['verification_code']).substring(3);
            $('#caller-id-verify-modal').modal('toggle');
            callerIDCheck = data['caller_id'];
            var checkStatus = setInterval(function(){
                var url = '/api/v1/campaigns/caller-ids/verify?callerid='+callerIDCheck;
                var jqxhr = $.get( url, function(data) {
                    console.log(data);
                    if(data != 'incomplete'){
                        clearInterval(checkStatus);
                        updateCallerIDs();
                        $('#caller-id-verify-modal').modal('hide');
                    }
                })
            },2000)
        },
        error: function(data){
            console.log('FAILURE');
        }
    });
});

var callerID;
$('body').on('click','.caller-id-delete', function(){
    callerID = $(this).attr('caller-id');
    console.log(callerID);
});

$('#caller-id-delete-conf').click(function(){
    var deleteData = {
        'id':callerID
    }
    console.log(deleteData);
    postToAPI('/api/v1/campaigns/caller-ids', deleteData, 'DELETE', 'updateCallerIDs');
})
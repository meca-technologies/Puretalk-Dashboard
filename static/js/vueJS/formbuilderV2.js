try{
    document.getElementById('form-builder-loading').style.display = '';
    document.getElementById('form-builder').style.display = 'none';
}catch(error){}
var formID;

var forms = new Vue({
    delimiters: ['[[', ']]'],
    el: '#form-builder',
    data: {
        forms:[]
    }
})

var formDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#form-edit',
    data: {
        details:{}
    }
})

var csvDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#form-details',
    data: {
        fields:[],
        columns:[],
        fullDetails:[]
    }
})

try{
    const inputElement = document.getElementById("import_file");
    inputElement.addEventListener("change", handleFiles, false);
}catch(error){}

var csvDataFull = [];
function handleFiles() {
    csvDetails.columns = [];
    csvDetails.fullDetails = [];
    const myFile = this.files[0]; /* now you can work with the file list */
    var reader = new FileReader();
    var parseData = [];
    reader.addEventListener('load', function (e) {
        var csvdata = e.target.result; 
        var lineBreaks = csvdata.split('\n');
        csvDataFull = lineBreaks;
        var columns = lineBreaks[0].split(',');
        csvDetails.columns = columns;
        for(var i = 0; i<csvDetails.columns.length; i++){
            csvDetails.fullDetails.push({
                'column_name':String(csvDetails.columns[i]).replace('\r', '').toUpperCase(),
                'fields':csvDetails.details
            })
        }
        console.log(csvDetails.fullDetails);
        console.log(csvDataFull);
        setTimeout(function(){
            var form_classes = document.getElementsByClassName("form-layout");
            for(var i = 0; i<form_classes.length; i++){
                $(form_classes[i]).removeClass('border-danger');
                if(form_classes[i].value == 'skip'){
                    $(form_classes[i]).addClass('border-danger');
                }
            }
        }, 200);
    });
    reader.readAsBinaryString(myFile);
}

function doneImporting(){
    document.getElementById("lead-import-loading").style.display = 'none';
    document.getElementById("lead-import-card").style.display = '';
}

$('body').on('change', '.form-layout', function(){
    var form_classes = document.getElementsByClassName("form-layout");
    for(var i = 0; i<form_classes.length; i++){
        $(form_classes[i]).removeClass('border-danger');
        if(form_classes[i].value == 'skip'){
            $(form_classes[i]).addClass('border-danger');
        }
    }
})

$('body').on('click','#importCSV', function(){
    var new_columns_class = document.getElementsByClassName("form-layout");
    var post_data = [];
    var list_id = $("#list-body").val();
    document.getElementById("lead-import-loading").style.display = '';
    document.getElementById("lead-import-card").style.display = 'none';
    for(var i = 1; i<csvDataFull.length; i++){
        var row = csvDataFull[i].split(',');
        var obj = {};
        obj['list_id'] = list_id;
        for(var j = 0; j<row.length; j++){
            if($(new_columns_class[j]).val()){
                if($(new_columns_class[j]).val() != 'skip' && $(new_columns_class[j]).val() != 'notUsed'){
                    var val = row[j];
                    val = val.split('/r').join('');
                    val = val.split('/n').join('');
                    val = val.split(' ').join('');
                    val = val.split('(').join('');
                    val = val.split(')').join('');
                    val = val.split('-').join('');
                    obj[$(new_columns_class[j]).val()] = val;
                }
            }
        }
        post_data.push(obj);
    }
    console.log(post_data);
    postToAPI('/api/vici/leads', post_data, 'POST', 'doneImporting');
})
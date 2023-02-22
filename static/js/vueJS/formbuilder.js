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

var leadImportStatus = new Vue({
    delimiters: ['[[', ']]'],
    el: '#lead-import-loading',
    data: {
        current:1,
        total:1
    }
})

function updateForms(){
    //$(".sidebar-transparent").click();
    var jqxhr = $.get( '/api/v1/forms?limit=2000', function(data) {
        forms.forms = data;
        try{
            document.getElementById('form-builder-loading').style.display = 'none';
            document.getElementById('form-builder').style.display = '';
        }catch(error){}
    }).always(function(){
        setTimeout(function(){
            updateNotification();
        },1000);
    });
}

$('body').on('click','.form-edit', function(){
    formID = $(this).attr('form-id');
    var url = '/api/v1/forms?formid='+formID;
    var jqxhr = $.get( url, function(data) {
        formDetails.details = data[0];
    })
});

function updateCurrentForm(){
    var url = '/api/v1/forms?formid='+formID;
    var jqxhr = $.get( url, function(data) {
        formDetails.details = data[0];
    })
}

$('#add-form').click(function(){
    document.getElementById('form-builder-loading').style.display = '';
    document.getElementById('form-builder').style.display = 'none';
    var postData = {
        'form_name':$('#form-name-add').val()
    }
    postToAPI('/api/v1/forms', postData, 'POST', 'updateForms');
})

$('#save-form').click(function(){
    var postData = {
        'id':formID,
        'form_name':$('#edit-form-name').val()
    }
    postToAPI('/api/v1/forms', postData, 'PUT', 'updateCurrentForm');
})

$('#edit-form-webhook').click(function(){
    var postData = {
        'id':formID,
        'webhook_url':$("#webhook_url").val(),
        'webhook_type':$("#webhook_type").val()
    }
    var webhook_fields = document.getElementsByClassName("webhook_fields");
    fields = [];
    for(var i = 0; i<webhook_fields.length; i++){
        fields.push({
            'field_name':$(webhook_fields[i]).attr("field-name"),
            'order':7,
            'webhook_field':$(webhook_fields[i]).val()
        })
    }
    if(fields.length>0){
        postData['fields'] = fields;
    }
    console.log(postData);
    postToAPI('/api/v1/forms', postData, 'PUT', 'updateCurrentForm');
})

$('body').on('click','.form-delete', function(){
    document.getElementById('form-builder-loading').style.display = '';
    document.getElementById('form-builder').style.display = 'none';
    var formID = $(this).attr('form-id');
    var deleteData = {
        'id':formID
    }

    postToAPI('/api/v1/forms', deleteData, 'DELETE', 'updateForms');
});

$('#add-label').click(function(){
    document.getElementById("form-edit-new-label-row").style.display = '';
    document.getElementById("add-label").style.display = 'none';
    document.getElementById("form-edit-buttons-row").style.display = '';
});

$('#cancel-label').click(function(){
    document.getElementById("form-edit-new-label-row").style.display = 'none';
    document.getElementById("add-label").style.display = '';
    document.getElementById("form-edit-buttons-row").style.display = 'none';
});

$('#save-label').click(function(){
    document.getElementById("form-edit-new-label-row").style.display = 'none';
    document.getElementById("add-label").style.display = '';
    document.getElementById("form-edit-buttons-row").style.display = 'none';
    var postData = {
        'id':formID,
        'fields':[]
    }
    var defaultForms = document.getElementsByClassName("default-forms");
    for(var i = 0; i<defaultForms.length; i++){
        if(defaultForms[i].checked){
            postData['fields'].push({
                'field_name':$(defaultForms[i]).attr('name'),
                'order':7
            })
        }
    }
    var defaultForms = document.getElementsByClassName("form_field");
    for(var i = 0; i<defaultForms.length; i++){
        var exists = false;
        for(var j = 0; j<postData['fields'].length; j++){
            if(postData['fields'][j]['field_name'] == $(defaultForms[i]).attr('name')){
                exists = true;
            }
        }
        if(exists){
            console.log("Exists");
        }
        else{
            postData['fields'].push({
                'field_name':$(defaultForms[i]).attr('name'),
                'order':7
            })
        }
    }
    postData['fields'].push({
        'field_name':$('#form-edit-new-label').val(),
        'order':7
    })
    postToAPI('/api/v1/forms', postData, 'PUT', 'updateCurrentForm');
});

$('body').on('click','.field-delete', function(){
    var parent = $(this).parent();
    parent.remove();
    var postData = {
        'id':$("#edit-form-id").val(),
        'fields':[]
    }
    var fields = document.getElementsByClassName("field-delete");
    for(var i = 0; i<fields.length; i++){
        postData['fields'].push({
            'field_name':$(fields[i]).attr('field-value'),
            'order':7
        })
    }
    console.log(postData);
    postToAPI('/api/v1/forms', postData, 'PUT', 'updateCurrentForm');
    //var fieldID = $(this).attr('field-id');
    //var deleteData = {
    //    'id':fieldID
    //}

    //postToAPI('/api/v1/forms/fields', deleteData, 'DELETE', 'updateCurrentForm');
});

$('body').on('click','.default-forms', function(){
    if(this.checked){
        formID = $(this).attr('form-id');
        var postData = {
            'id':formID,
            'fields':[{
                'field_name':$(this).attr('name'),
                'order':7
            }]
        }
        postData['fields'] = []
        var defaultForms = document.getElementsByClassName("default-forms");
        for(var i = 0; i<defaultForms.length; i++){
            if(defaultForms[i].checked){
                postData['fields'].push({
                    'field_name':$(defaultForms[i]).attr('name'),
                    'order':7
                })
            }
        }
        var defaultForms = document.getElementsByClassName("form_field");
        for(var i = 0; i<defaultForms.length; i++){
            var exists = false;
            for(var j = 0; j<postData['fields'].length; j++){
                if(postData['fields'][j]['field_name'] == $(defaultForms[i]).attr('name')){
                    exists = true;
                }
            }
            if(exists){
                console.log("Exists");
            }
            else{
                postData['fields'].push({
                    'field_name':$(defaultForms[i]).attr('name'),
                    'order':7
                })
            }
        }

        console.log(JSON.stringify(postData));
        postToAPI('/api/v1/forms', postData, 'PUT', 'updateCurrentForm');
    }
    else{
        this.checked = true;
    }
});

updateForms();

var csvDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#form-details',
    data: {
        fields:[],
        columns:[],
        fullDetails:[],
        field_mappings:{}
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
            var full_detail_temp = {
                'column_name':csvDetails.columns[i],
                'fields':csvDetails.details
            }

            try{
                full_detail_temp['selected_field'] = csvDetails.field_mappings[csvDetails.columns[i]];
            }catch(error){}

            csvDetails.fullDetails.push(full_detail_temp)
        }
    });
    reader.readAsBinaryString(myFile);
}


$('#campaign-body').change(function(){
    console.log('CHANGED');
    var campaignID = $(this).val();
    csvDetails.fields = [];
    csvDetails.fullDetails = [];
    var jqxhr = $.get( '/api/v1/campaigns?campaignid='+campaignID, function(data) {
        var newFormID = data[0]['form_id'];
        var url = '/api/v1/forms?formid='+newFormID;
        var jqxhr = $.get( url, function(data) {
            csvDetails.field_mappings = data[0]['field_mappings']
            csvDetails.details = data[0]['fields'];
            csvDetails.fullDetails = [];
            for(var i = 0; i<csvDetails.columns.length; i++){
                var full_detail_temp = {
                    'column_name':csvDetails.columns[i],
                    'fields':csvDetails.details
                }

                try{
                    full_detail_temp['selected_field'] = csvDetails.field_mappings[csvDetails.columns[i]];
                }catch(error){}

                csvDetails.fullDetails.push(full_detail_temp);
                //csvDetails.fullDetails.push({
                //    'column_name':csvDetails.columns[i],
                //    'fields':csvDetails.details
                //})
            }
            console.log(csvDetails.fullDetails);
        })
    })
})

$('body').on('change','.form-layout', function(){
    var change_val = $(this).val();
    var columnLayoutSelects = $(".form-layout");
    var counts = 0;
    for(var i = 0; i<columnLayoutSelects.length; i++){
        if(columnLayoutSelects[i].value == change_val){
            counts+=1;
        }
    }
    if(counts > 1){
        $(this).addClass('border-danger');
        p_tag = $(this).parent().find('p').css( "display", "" );
        $("#importCSV").prop( "disabled", true );
    }
    else{
        $(this).removeClass('border-danger');
        p_tag = $(this).parent().find('p').css( "display", "none" );
        $("#importCSV").prop( "disabled", false );
    }
})

$('body').on('click','#importCSV', function(){
    document.getElementById("lead-import-loading").style.display = '';
    document.getElementById("lead-import-card").style.display = 'none';
    console.log('CLicked');
    var columnLayoutSelects = $(".form-layout");
    var columnLayout = [];

    var numColumns = csvDataFull[0].split(',').length;

    for(var i = 0; i<columnLayoutSelects.length; i++){
        columnLayout.push({
            "field_name":$(columnLayoutSelects[i]).find("option:selected").text()
        });
    }
    var campaignID = $("#campaign-body").val();
    var postData = [];

    leadImportStatus.current = 0;
    leadImportStatus.total = 1;
    for(var i = 1; i<csvDataFull.length; i++){
        var leadData = [];
        var columns = csvDataFull[i].split(',');
        var referenceNumber = "";
        for(var j = 0; j<columns.length; j++){
            try{
                if(columnLayout[j]['form_field_id'] != 'refNum'){
                    if(columnLayout[j]['form_field_id'] != 'skip' && columnLayout[j]['form_field_id'] != 'notUsed'){
                        console.log(columnLayout[j]['field_name'])
                        if(columnLayout[j]['field_name'] != 'Please Select A Field' && columnLayout[j]['field_name'] != '- Not Used -'){
                            leadData.push({
                                //"form_field_id":columnLayout[j]['form_field_id'],
                                "field_name":columnLayout[j]['field_name'],
                                "field_value":columns[j]
                            });
                        }
                    }
                }
                else{
                    referenceNumber = columns[j];
                }
            }catch(error){}
        }
        if(leadData.length > 0){
            postData.push({
                "reference_number":referenceNumber,
                "status":"unactioned",
                "interested":null,
                "appointment_booked":"0",
                "campaign_id":campaignID,
                "email_template_id":null,
                "first_actioned_by":null,
                "last_actioned_by":null,
                "time_taken":null,
                "lead_data":leadData
            })
        }
    }
    console.log(postData);
    if(postData.length > 5000){
        var post_length = postData.length;
        var increment = Math.ceil(post_length/100);
        leadImportStatus.total = increment;
        for(var i = 0; i<increment; i++){
            var splitPost = postData.slice((100*i), (i*100)+100);
            postToAPI('/api/v1/leads', splitPost, 'POST', 'getLeadStatus');
        }
    }
    else{
        postToAPI('/api/v1/leads', postData, 'POST', 'reloadPage');
    }
    //postToAPI('/api/v1/forms', splitPost, 'PUT', 'doNothing');
})

function getLeadStatus(){
    var current = leadImportStatus.current;
    var total = leadImportStatus.total;
    current += 1;
    leadImportStatus.current = current;
    console.log(current);
    console.log(total);
    
    calculateProgressBars();
    if(current == total){
        console.log('Done Importing')
        location.reload();
    }
}

/** FIELD MAPPINGS **/

var fieldMappingDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#field-mapping-table',
    data: {
        field_mappings:{},
        fields:[]
    }
})

$('body').on('change','.form-builder', function(){
    formID = $(this).val();
    var url = '/api/v1/forms?formid='+formID;
    var jqxhr = $.get( url, function(data) {
        fieldMappingDetails.field_mappings = data[0]['field_mappings'];
        fieldMappingDetails.fields = data[0]['fields'];
        fieldMappingDetails.fields.push({
            "field_name": "IGNORED"
        })
        document.getElementById("field-mapping-wrapper").style.display = '';
    })
});

function getCurrentMappings(){
    var selected_field_csvs = document.getElementsByClassName("selected_field_csv");
    var selected_field_forms = document.getElementsByClassName("selected_field_form");

    var field_mappings = {};
    for(var i = 0; i<selected_field_csvs.length; i++){
        field_mappings[selected_field_csvs[i].value] = selected_field_forms[i].value;
    }
    return field_mappings;
}

$('body').on('click','#save-field-mapping', function(){
    var postData = {
        'id':$("#form-builder").val(),
        'field_mappings':getCurrentMappings()
    }
    console.log(JSON.stringify(postData));
    postToAPI('/api/v1/forms', postData, 'PUT', 'doNothing');
});

$('body').on('click','#add-field-mapping', function(){
    field_mappings = getCurrentMappings();
    field_mappings['test'] = 'test';
    fieldMappingDetails.field_mappings = field_mappings;
})

$('body').on('click','.delete-field-mapping', function(){
    var del_index = $(this).attr("index");
    var selected_field_csvs = document.getElementsByClassName("selected_field_csv");

    field_mappings = getCurrentMappings()
    delete field_mappings[$(selected_field_csvs[del_index]).val()];
    fieldMappingDetails.field_mappings = field_mappings;
})
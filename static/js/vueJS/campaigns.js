try{
    document.getElementById('campaign-body-loading').style.display = '';
    document.getElementById('campaign-body').style.display = 'none';
}catch(error){}
try{
    document.getElementById('campaign-edit-loading').style.display = '';
    document.getElementById('campaign-edit-body').style.display = 'none';
}catch(error){}

var code_editor;
var campaignID;
var campaigns = new Vue({
    delimiters: ['[[', ']]'],
    el: '#campaign-body',
    data: {
        campaigns:[]
    }
})

var campaignDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#campaign-edit',
    data: {
        details:{},
        virtualAgents:[],
        caller_ids:[],
        form:{},
        headers:[
            {
                "field":"",
                "value":""
            }
        ],
        params:[
            {
                "field":"",
                "value":""
            }
        ],
        payload:'{\n\t\n}'
    }
})

var requestDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#request-test',
    data: {
        form:{}
    }
})

var campaignTesting = new Vue({
    delimiters: ['[[', ']]'],
    el: '#campaign-test',
    data: {
        status:'No Call'
    }
})

var campaign_table;

function updateCampaigns(useAjax=true, updateCallManager=false, getSummary=true, status){
    $(".sidebar-transparent").trigger('click');;
    if(useAjax){
        try{
            document.getElementById('campaign-body-loading').style.display = '';
            document.getElementById('campaign-body').style.display = 'none';
        }catch(error){}
        var url = '/api/v1/campaigns?limit=2000';
        if(getSummary){
            url += '&summary=1';
        }
        if(status){
            url += '&status='+status;
        }

        var jqxhr = $.get( url, function(data) {
            console.log(data);
            campaigns.campaigns = data;
            if(updateCallManager){
                callCampaigns.campaigns = data;
            }
            try{
                document.getElementById('campaign-body-loading').style.display = 'none';
                document.getElementById('campaign-body').style.display = '';
            }catch(error){}
            try{
                campaign_table.destroy();
            }catch(error){}
        }).always(function(){
            try{
                document.getElementById('campaign-body-loading').style.display = 'none';
                document.getElementById('campaign-body').style.display = '';
            }catch(error){}
            setTimeout(function(){
                try{
                    campaign_table = $('#campaign-body').DataTable({
                        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
                        "pageLength": 20,
                        "language": {
                            "paginate": {
                                "previous": "<<",
                                "next": ">>"
                            }
                        },
                        initComplete: function() {
                            $(this.api().table().container()).find('input[type="search"]').parent().wrap('<form>').parent().attr('autocomplete','off').css('overflow','hidden').css('margin','auto');
                        }   
                    });
                }catch(error){}
                calculateProgressBars();
                try{
                    updateNotification();
                }catch(error){}
            },1000);
        });
    }
    else{
        try{
            document.getElementById('campaign-body-loading').style.display = 'none';
            document.getElementById('campaign-body').style.display = '';
        }catch(error){}
        setTimeout(function(){
            calculateProgressBars();
            updateNotification();
        },1000);
    }
    var jqxhr = $.get( '/api/v1/virtual-agents?limit=2000', function(data) {
        campaignDetails.virtualAgents = data;
    });

    // GRAB CALLER IDS
    var url = '/api/v1/campaigns/caller-ids';
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        campaignDetails.caller_ids = data;
    })
}

$('#add-company').click(function(){
    if(validateForm(['#addCampaignName'])){
        postData = {
            "name":$('#addCampaignName').val(),
            "status":'paused',
            "started_on":null,
            "total_leads":0,
            "remaining_leads":0,
            "auto_reference":document.getElementById('addCampaignARE').checked ? 1:0,
            "form_id":$('#addCampaignForm').val(),
            "auto_reference_prefix":$('#addCampaignARP').val(),
            "user_data":[]
        }
        var campaignAddUsers = document.getElementsByClassName('campaignAddUser');
        for(var i = 0; i<campaignAddUsers.length; i++){
            postData['user_data'].push({
                'user_id':$(campaignAddUsers[i]).attr('user-id')
            })
        }
        console.log(postData);
        try{
            document.getElementById('campaign-body-loading').style.display = '';
            document.getElementById('campaign-body').style.display = 'none';
        }catch(error){}
        postToAPI('/api/v1/campaigns', postData, 'POST', 'updateCampaigns');
    }
});

$('body').on('click','#add-caller-id', function(){
    var _this = $("#campaignEditCallerID");
    var caller_ids = [];
    var caller_id_doms = document.getElementsByClassName("caller-id-list-item");
    for(var i = 0; i<caller_id_doms.length; i++){
        caller_ids.push({
            'caller_id':$(caller_id_doms[i]).attr('cid'),
            'name':$(caller_id_doms[i]).attr('cid')
        })
    }
    var new_caller_id = $('option:selected', _this).attr("cid");
    var new_caller_id_name = $('option:selected', _this).attr("ciname");
    var post_this = false;
    if(new_caller_id !== undefined && new_caller_id){
        caller_ids.push({
            'caller_id':new_caller_id,
            'name':new_caller_id_name
        })
        post_this = true;
    }
    var postData = {
        'id':campaignID,
        'caller_ids':caller_ids
    }
    console.log(postData);
    if(post_this){
        $(_this).removeClass('border-danger');
        postToAPI('/api/v1/campaigns', postData, 'PUT', 'campaignEditUpdate');
    }
    else{
        $(_this).addClass('border-danger');
    }
});

$('body').on('click','.caller-id-list-item-delete', function(){
    $(this).parent().remove();
    var caller_ids = [];
    var caller_id_doms = document.getElementsByClassName("caller-id-list-item");
    for(var i = 0; i<caller_id_doms.length; i++){
        caller_ids.push({
            'caller_id':$(caller_id_doms[i]).attr('cid'),
            'name':$(caller_id_doms[i]).attr('cid')
        })
    }
    var postData = {
        'id':campaignID,
        'caller_ids':caller_ids
    }
    console.log(postData);
    postToAPI('/api/v1/campaigns', postData, 'PUT', 'campaignEditUpdate');
})

$('body').on('click','#edit-company', function(){
    try{
        document.getElementById('campaign-edit-loading').style.display = '';
        document.getElementById('campaign-edit-body').style.display = 'none';
    }catch(error){}
    var agentTypes = $('.agent-type');
    var agentType = $(agentTypes[0]).hasClass('active');
    var numAgents = 1;
    var callsPerAgent = 1;
    if(agentType){
        numAgents = 0;
        callsPerAgent = $('#total-calls').val();
    }
    else{
        numAgents = $('#num-agent').val();
        callsPerAgent = $('#calls-per-agent').val();
    }
    var postData = {
        'id':campaignID,
        'name':$('#campaignEditName').val(),
        'schedule_data':[],
        'num_agents':numAgents,
        'calls_per_agent':callsPerAgent,
        'headers':campaignDetails.headers,
        'params':campaignDetails.params,
        'payload':code_editor.getValue(),
        'did':$("#campaignEditDID").val(),
        'xfer_method':$("#campaign-request-method").val(),
        'xfer_url':$("#campaign-xfer-url").val(),
        'white_url':$("#campaign-white-url").val(),
        'agent_login':document.getElementById('campaignEditAgentLogin').checked ? true:false
    }
    var timers = $(".timer");
    var switches = $(".dayEnabled");
    for(var i = 0; i<timers.length; i++){
        var id = $(timers[i]).attr('day-value')+'Enabled';
        console.log(id);
        postData['schedule_data'].push({
            "day_value":$(timers[i]).attr('day-value'),
            "status":$(timers[i]).attr('day-status'),
            "time_full":convertTime($(timers[i]).val()),
            'enabled':document.getElementById(id).checked ? true:false
        })
    }
    if($("#virtual-agent-body").val() != 'None'){
        postData['virtual_agent_id'] = $("#virtual-agent-body").val();
    }
    if($("#campaignEditCallerID").val() != 'None'){
        postData['caller_id'] = $("#campaignEditCallerID").val();
    }
    console.log(postData);
    postToAPI('/api/v1/campaigns', postData, 'PUT', 'updateCampaigns');
});

$('body').on('click','.campaign-delete', function(){
    campaignID = $(this).attr('campaign-id');
    try{
        document.getElementById('campaign-body-loading').style.display = '';
        document.getElementById('campaign-body').style.display = 'none';
    }catch(error){}
    var postData = {
        'id':campaignID
    }
    try{
        document.getElementById('campaign-body-loading').style.display = '';
        document.getElementById('campaign-body').style.display = 'none';
    }catch(error){}
    postToAPI('/api/v1/campaigns', postData, 'DELETE', 'updateCampaigns');
});

$('body').on('click','.campaign-edit', function(){
    campaignID = $(this).attr('campaign-id');
    campaignEditUpdate();
});

function campaignEditUpdate(){
    try{
        $("div[tab-target='transfers-body-tab']").trigger('click');
    }catch(error){}
    var url = '/api/v1/campaigns?campaignid='+campaignID;
    console.log(url);
    try{
        document.getElementById('campaign-edit-loading').style.display = '';
        document.getElementById('campaign-edit-body').style.display = 'none';
    }catch(error){}
    var jqxhr = $.get( url, function(data) {
        campaignDetails.details = data[0];
        try{
            if(data[0]['headers']){
                campaignDetails.headers = data[0]['headers'];
            }
            else{
                campaignDetails.headers = [
                    {
                        "field":"",
                        "value":""
                    }
                ];
            }
        }catch(error){
            campaignDetails.headers = [
                {
                    "field":"",
                    "value":""
                }
            ];
        }
        try{
            if(data[0]['params']){
                campaignDetails.params = data[0]['params'];
            }
            else{
                campaignDetails.params = [
                    {
                        "field":"",
                        "value":""
                    }
                ];
            }
        }catch(error){
            campaignDetails.params = [
                {
                    "field":"",
                    "value":""
                }
            ];
        }
        try{
            if(data[0]['payload']){
                campaignDetails.payload = data[0]['payload'];
            }
            else{
             
                campaignDetails.payload = '{\n\t\n}';
            }
        }catch(error){
            campaignDetails.payload = '{\n\t\n}';
        }
        console.log(campaignDetails);
        if(data[0]['num_agents'] == 0 && data[0]['calls_per_agent'] > 0){
            $("#tab1").trigger('click');;
        }
        else{
            $("#tab2").trigger('click');;
        }
        var form_url = '/api/v1/forms?formid='+data[0]['form_id'];
        var jqxhr = $.get( form_url, function(data) {
            console.log(data);
            requestDetails.form = data[0];
            campaignDetails.form = data[0];
        });
    }).always(function(){
        setTimeout(function(){
            try{
                try{
                    var codeMirrors = document.getElementsByClassName("CodeMirror");
                    for(var i = 0; i<codeMirrors.length; i++){
                        codeMirrors[i].remove();
                    }
                }catch(error){}
                code_editor = CodeMirror.fromTextArea(document.getElementById("code"), {
                    lineNumbers: true,
                    styleActiveLine: true,
                    matchBrackets: true
                });
                
                var theme = 'isotope';
                code_editor.setOption("theme", theme);
                location.hash = "#" + theme;
            
                var choice = (location.hash && location.hash.slice(1)) ||
                            (document.location.search &&
                            decodeURIComponent(document.location.search.slice(1)));
                if (choice) {
                    input.value = 'isotope';
                    code_editor.setOption("theme", choice);
                }
                CodeMirror.on(window, "hashchange", function() {
                var theme = location.hash.slice(1);
                if (theme) { input.value = theme; selectTheme(); }
                });
            }catch(error){}
            $('.datetimepicker').datetimepicker({
                icons: {
                    time: "fa fa-clock",
                    date: "fa fa-clock",
                    up: "fa fa-chevron-up",
                    down: "fa fa-chevron-down",
                    previous: 'fa fa-chevron-left',
                    next: 'fa fa-chevron-right',
                    today: 'fa fa-screenshot',
                    clear: 'fa fa-trash',
                    close: 'fa fa-remove'
                },
                format: 'LT'
            });
            try{
                document.getElementById('campaign-edit-loading').style.display = 'none';
                document.getElementById('campaign-edit-body').style.display = '';
            }catch(error){}
            setTimeout(function(){
                try{
                    var codeMirrors = document.getElementsByClassName("CodeMirror");
                    for(var i = 0; i<codeMirrors.length; i++){
                        $(codeMirrors[i]).trigger('click');;
                        console.log('Click');
                        code_editor.refresh();
                    }
                }catch(error){}
            }, 2000)
        }, 1000)
    })
}


var curr_search_bar;
var curr_index;
var curr_type = 'Header';
function searchVariables(search_bar_id, search_bar_div_id, search_bar_variable_body, search_value){
    if(search_value.substring(0,1) == '['){
        document.getElementById(search_bar_div_id).style.display = '';
        console.log(search_value);
        search_value = search_value.replace('[', '');
        search_value = search_value.replace(']', '');
        console.log(search_value);
        document.getElementById(search_bar_id).innerHTML = search_value;

        filter = search_value.toUpperCase();
        div = document.getElementById(search_bar_variable_body);
        a = div.getElementsByTagName("div");
        for (i = 0; i < a.length; i++) {
            txtValue = a[i].textContent || a[i].innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                a[i].style.display = "";
            } else {
                a[i].style.display = "none";
            }
        }
    }
    else{
        document.getElementById(search_bar_div_id).style.display = 'none';
        console.log(search_value);
        document.getElementById(search_bar_id).innerHTML = '';
    }
}

/** HEADER STUFF **/
$('body').on('click','#add-header', function(){
    campaignDetails.headers.push({
        "field":"",
        "value":""
    })
})

$('body').on('click','.sub-header-btn', function(){
    console.log($(this).attr("header-index"));
    campaignDetails.headers.splice($(this).attr("header-index"), 1);
})

$('body').on('keyup','.header-form-field', function(){
    var header_index = $(this).attr("header-index");
    var header_val = $(this).val();
    campaignDetails.headers[header_index]['field'] = header_val
})

$('body').on('keyup','.header-form-value', function(){
    var header_index = $(this).attr("header-index");
    var header_val = $(this).val();
    campaignDetails.headers[header_index]['value'] = header_val;

    curr_type = 'Header';
    curr_search_bar = this;
    curr_index = header_index;
    var search_bar_id = header_index + '-search';
    var search_bar_div_id = header_index + '-search-div';
    var search_bar_variable_body = header_index + '-header-variable-body'
    search_value = $(this).val();
    searchVariables(search_bar_id, search_bar_div_id, search_bar_variable_body, search_value);
})

$('body').on('click','.variable-item', function(){
    console.log(curr_search_bar);
    console.log(curr_index);
    curr_search_bar.value = '[' + $(this).attr('variable') + ']';
    $(this).parent().parent().parent().css('display', 'none');
    
    if(curr_type == 'Header'){
        campaignDetails.headers[curr_index]['value'] = curr_search_bar.value;
    }
    else{
        campaignDetails.params[curr_index]['value'] = curr_search_bar.value;
    }
});

/** PARAM STUFF **/
$('body').on('click','#add-param', function(){
    campaignDetails.params.push({
        "field":"",
        "value":""
    })
})

$('body').on('click','.sub-param-btn', function(){
    console.log($(this).attr("param-index"));
    campaignDetails.params.splice($(this).attr("param-index"), 1);
})

$('body').on('keyup','.params-form-field', function(){
    var param_index = $(this).attr("param-index");
    var param_val = $(this).val();
    campaignDetails.params[param_index]['field'] = param_val
})

$('body').on('keyup','.params-form-value', function(){
    var param_index = $(this).attr("param-index");
    var param_val = $(this).val();
    campaignDetails.params[param_index]['value'] = param_val;

    curr_type = 'Param';
    curr_search_bar = this;
    curr_index = param_index;
    var search_bar_id = curr_index + '-param-search';
    var search_bar_div_id = curr_index + '-param-search-div';
    var search_bar_variable_body = curr_index + '-param-variable-body'
    search_value = $(this).val();
    searchVariables(search_bar_id, search_bar_div_id, search_bar_variable_body, search_value);
})

$("div[tab-target='transfers-body-tab']").click(function(){
    code_editor.refresh();
});

$('body').on('click','#send-request', function(){
    console.log('Clicked');
    console.log(code_editor.getValue());

    //HEADERS
    var request_headers = campaignDetails.headers;

    // PAYLOAD
    var request_body = code_editor.getValue();
    var value_split = request_body.split('\t')
    request_body = value_split.join('');
    value_split = request_body.split('\n')
    request_body = value_split.join('');

    var request_payload = {};
    var variables_request = document.getElementsByClassName("variable-form");

    //PARAMS
    var request_params = campaignDetails.params;

    for(var i = 0; i<variables_request.length; i++){
        var varname = $(variables_request[i]).attr('varname');
        request_payload[varname] = $(variables_request[i]).val();
    }
    var post_data = {
        'request_method':$("#campaign-request-method").val(),
        'request_url':$("#campaign-xfer-url").val(),
        'request_body':request_body,
        'request_headers':JSON.stringify(request_headers),
        'request_payload':JSON.stringify(request_payload),
        'request_params':JSON.stringify(request_params)
    }
    console.log(post_data);
    postToAPI('/api/v1/campaigns/test-hook', post_data, 'POST', 'getTestResponse')
})

$('body').on('click','#request-test-btn', function(){
    $("#request-test").removeClass("bd-example-modal-xl");
    $("#request-test-dialog").removeClass("modal-xl");
    document.getElementById("variables-body").style.display = '';
    document.getElementById("response-body").style.display = 'none';
    document.getElementById("code-response").value = '{\n\n}';
})

//updateCampaigns();

$('body').on('click','.lead-export', function(){
    var url = '/api/v1/leads/export?campaignid='+$(this).attr('campaign-id');
    var csv = '';
    var jqxhr = $.get( url, function(data) {
        console.log(data.length);
        for(var i = 0; i<data.length; i++){
            for(var j = 0; j<data[i].length; j++){
                data[i][j] = data[i][j].split('"').join("");
                data[i][j] = data[i][j].split("'").join("");
                data[i][j] = data[i][j].split("#").join("");
            }
            csv += data[i].join(',');
            csv += "\n";
        }
        //data.forEach(function(row) {
        //    csv += row.join(',');
        //    csv += "\n";
        //});
        console.log(csv);
        var hiddenElement = document.createElement('a');
        hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
        hiddenElement.target = '_blank';
        hiddenElement.download = 'leads.csv';
        hiddenElement.trigger('click');;
    })
});

$('body').on('click','.campaign-test', function(){
    campaignID = $(this).attr('campaign-id');
});

$("#call-now-test").click(function(){
    var ref_num = $("#test-phone").val();
    if(String(ref_num).substring(0, 2) != '+1'){
        ref_num = '+1'+ref_num;
    }
    var post_data = {
        'reference_number':ref_num,
        'campaign_id':campaignID
    }
    console.log(post_data);
    postToAPI('/api/v1/twilio/test_call', post_data, 'POST', 'doNothing');
    setTimeout(function(){
        var call_status_check = setInterval(function(){
            var url = '/api/v1/twilio/test_call';
            var jqxhr = $.get( url, function(data) {
                campaignTesting.status = data['Status'];
                if(data['Status'] == 'completed' || data['Status'] == 'failed' || data['Status'] == 'unreachable' || data['Status'] == 'no-answer'){
                    clearInterval(call_status_check);
                }
            });
        }, 1500)
    },2000)
});

function convertTime(x){
    x = '2021-01-01 ' + x;
    var d = new Date(x);
    var hour = addZero(d.getHours());
    var minutes = addZero(d.getMinutes());
    return hour + ':' + minutes + ':00';
}

function convertNiceTime(x){
    x = '2021-01-01 ' + x;
    var d = new Date(x);
    var hour = d.getHours() > 12 ? (d.getHours()-12): (d.getHours());
    var amPM = d.getHours() > 11 ? 'PM':'AM';
    var minutes = addZero(d.getMinutes());
    return hour + ':' + minutes + ' ' + amPM;
}

function getFlatCall(x,y){
    if(x == 0){
        x = 1;
    }
    return x*y;
}

function formatAgentLogin(id, name){
    return '/agent-login?campaignid='+id+'&campaignname='+name;
}

function getTestResponse(req_data){
    $("#request-test").addClass("bd-example-modal-xl");
    $("#request-test-dialog").addClass("modal-dialog modal-xl");
    document.getElementById("variables-body").style.display = 'none';
    document.getElementById("response-body").style.display = '';
    var json_str = JSON.stringify(req_data['Response'], null, 4)
    console.log(json_str);
    document.getElementById("code-response").innerHTML = json_str
}
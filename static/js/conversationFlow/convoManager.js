var conversation = new Vue({
    delimiters: ['[[', ']]'],
    el: '#vf-canvas',
    data: {
        'holders':[],
        'id':'',
        'canvas_translate':'translate(0px, 0px)'
    }
});

var nlu_details = new Vue({
    delimiters: ['[[', ']]'],
    el: '#nlu-model',
    data: {
        "intent":{
            "intents":[{
                "name":"Item 1",
                "examples":[{
                    'label':'Intent One {test}',
                    'id':'hddnl'
                }]
            }],
            "details":{}
        }
    }
});

var canvas_details = new Vue({
    delimiters: ['[[', ']]'],
    el: '#canvas-details',
    data: {
        "zoom":"100%"
    }
});

var header_editor = new Vue({
    delimiters: ['[[', ']]'],
    el: '#header-details',
    data: {
        "details":{}
    }
})

var speech_editor = new Vue({
    delimiters: ['[[', ']]'],
    el: '#convo-details',
    data: {
        "details":{}
    }
})

var choice_editor = new Vue({
    delimiters: ['[[', ']]'],
    el: '#choice-details',
    data: {
        "details":{},
        "intents":[]
    }
})

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const flowid = urlParams.get('flowid')
var url = '/api/v1/flows?flowid='+flowid;
console.log(flowid);
var jqxhr = $.get(url, function(data) {
    conversation['holders'] = data[0]['holders'];
    conversation['id'] = data[0]['id'];
    conversation['canvas_translate'] = data[0]['canvas_translate'];
    nlu_details['intent']['intents'] = data[0]['intents'];
    console.log(data[0]['intents'])
    setTimeout(function(){
        curr_trans = conversation['canvas_translate'];
        document.getElementById('vf-canvas').style.transform = curr_trans + ' ' + curr_scale;
        getCoordinates();
    }, 100)
})

setInterval(function(){
    //saveFlow();
}, 30000);

function saveFlow(){
    $("#saving-card").fadeIn(200);
    var payload = {
        'holders':conversation['holders'],
        'id':conversation['id'],
        'canvas_translate':conversation['canvas_translate'],
        'intents':nlu_details['intent']['intents']
    }
    var url = '/api/v1/flows';
    var type = 'PUT';
    $.ajax({
        type: type,
        url: url,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: JSON.stringify(payload),
        success: function(data){
            getCoordinates();
            setTimeout(function(){
                $("#saving-card").fadeOut(200);
            }, 2000);
        },
        error: function(data){
            getCoordinates();
            console.log('FAILURE');
            setTimeout(function(){
                $("#saving-card").fadeOut(200);
            }, 2000);
        }
    })
}

$("#export-nlu").click(function(){
    var yaml_json = {
        "version":"2.0",
        "nlu":[]
    }
    for(var i = 0; i<nlu_details['intent']['intents'].length; i++){
        var intent_json = {
            "intent":nlu_details['intent']['intents'][i]['name'],
            "examples":[]
        }
        for(var j = 0; j<nlu_details['intent']['intents'][i]['examples'].length; j++){
            intent_json['examples'].push(nlu_details['intent']['intents'][i]['examples'][j]['label']);
        }
        yaml_json['nlu'].push(intent_json)   
    }
    var url = '/api/v1/j2y';
    var type = 'POST';
    $.ajax({
        type: type,
        url: url,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: JSON.stringify(yaml_json),
        success: function(data){
            
        },
        error: function(data){
        }
    })
})
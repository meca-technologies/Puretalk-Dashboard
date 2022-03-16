/** HEADER LABEL **/
$('body').on('click','.header-item', function(){
    var holder_index = $(this).attr('holder-index');
    header_editor['details'] = conversation['holders'][holder_index];
    header_editor['details']['holder_index'] = holder_index;
    console.log(header_editor['details']);
});

$('body').on('keyup','#edit-header-label', function(e){
    console.log(e.keyCode);
    if(e.keyCode == 13){
        $("#header-details").fadeOut(200);
        saveHeader();
    }
})

$("#edit-header").click(function(){
    saveHeader();
})

function saveHeader(){
    var holder_index = header_editor['details']['holder_index'];
    conversation['holders'][holder_index]['label'] = $("#edit-header-label").val();
    saveFlow();
}

/** SPEECH EDIT **/
$('body').on('click','.speech-item', function(){
    var holder_index = $(this).attr('holder-index');
    var row_index = $(this).attr('row-index');
    speech_editor['details'] = conversation['holders'][holder_index]['items'][row_index];
    speech_editor['details']['holder_index'] = holder_index;
    speech_editor['details']['row_index'] = row_index;
    console.log(speech_editor['details']);
});

$('body').on('keyup','#edit-label', function(e){
    console.log(e.keyCode);
    if(e.keyCode == 13){
        $("#convo-details").fadeOut(200);
        saveLabel();
    }
})

$("#edit-speech").click(function(){
    saveLabel();
})

function saveLabel(){
    var holder_index = speech_editor['details']['holder_index'];
    var row_index = speech_editor['details']['row_index'];
    conversation['holders'][holder_index]['items'][row_index]['label'] = $("#edit-label").val();
    saveFlow();
}

/** CHOICE EDIT **/
$('body').on('click','.choice-item', function(){
    var holder_index = $(this).attr('holder-index');
    var row_index = $(this).attr('row-index');
    var conv_details = conversation['holders'][holder_index]['items'][row_index];
    choice_editor['details'] = conv_details;
    choice_editor['intents'] = nlu_details['intent']['intents'];
    choice_editor['details']['holder_index'] = holder_index;
    choice_editor['details']['row_index'] = row_index;
    console.log(choice_editor['details']);
});

$("#add-choice").click(function(){
    choice_editor['details']['choices'].push({
        'id':generateID(),
        'label':'New Choice',
        'intent':'',
        'anchor_from':null,
        'anchor_to':null,
    });
    setTimeout(function(){
        getCoordinates();
    }, 100)
})

$('body').on('click','.delete-choice', function(){
    var choice_index = $(this).attr('choice-index');
    choice_editor['details']['choices'].splice(choice_index, 1); 
    setTimeout(function(){
        getCoordinates();
    }, 100)
})

$('body').on('keyup','.choice-label', function(e){
    var choice_index = $(this).attr('choice-index');
    choice_editor['details']['choices'][choice_index]['label'] = $(this).val();
})

$("#edit-choice").click(function(){
    saveChoice();
})

function saveChoice(){
    var holder_index = choice_editor['details']['holder_index'];
    var row_index = choice_editor['details']['row_index'];
    choice_editor['details']['label'] = $("#edit-choice-label").val();
    
    var choice_labels = document.getElementsByClassName("choice-label");
    for(var i = 0; i<choice_labels.length; i++){
        var indx = $(choice_labels[i]).attr('choice-index');
        choice_editor['details']['choices'][indx]['label'] = $(choice_labels[i]).val();
    }
    var choice_intents = document.getElementsByClassName("choice-intent");
    for(var i = 0; i<choice_intents.length; i++){
        var indx = $(choice_intents[i]).attr('choice-index');
        choice_editor['details']['choices'][indx]['intent'] = $(choice_intents[i]).val();
    }
    conversation['holders'][holder_index]['items'][row_index] = choice_editor['details'];
    saveFlow();
}

/** SPEECH ADD **/
var add_holder_index;
$('body').on('click','.edit-convo-card-btn', function(){
    add_holder_index = $(this).attr('holder-index');
});

$('body').on('keyup','#add-speech-label', function(e){
    if(e.keyCode == 13){
        addSpeech();
    }
})

$("#add-speech").click(function(){
    addSpeech();
})

function addSpeech(){
    var add_speech = {
        "id":generateID(),
        "index":0,
        "label":$("#add-speech-label").val(),
        "type":"speak",
        "holder_index":add_holder_index,
        "row_index":0
    };
    conversation['holders'][add_holder_index]['items'].push(add_speech);
    $("#convo-details").fadeOut(200);
    saveFlow();
    $("#add-speech-label").val('');
}

/** BLOCK EDITOR **/
$("#delete-block").click(function(){
    conversation['holders'].splice(add_holder_index, 1);
    saveFlow();
})
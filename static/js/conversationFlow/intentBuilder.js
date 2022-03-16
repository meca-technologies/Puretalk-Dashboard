nlu_details.intent.details = nlu_details.intent.intents[0]; 
nlu_details.intent.details.parent_index = 0;

$('body').on('click','.intent-row', function(){
    var index = parseInt($(this).attr('index'));
    console.log(index);
    nlu_details.intent.details = nlu_details.intent.intents[index];
    nlu_details.intent.details.parent_index = index;
    
    var nlu_rows = document.getElementsByClassName("intent-row");
    for(var i = 0; i<nlu_rows.length; i++){
        $(nlu_rows[i]).removeClass('active');
        if(i == index){
            $(nlu_rows[i]).addClass('active');
        }
    }
});

/************** NEW Examples For Intents **************/
$('body').on('keyup','#intent-name', function(){
    var parent_index = parseInt($(this).attr('parent-index'));
    nlu_details.intent.intents[parent_index].name = $(this).val();
})

$('body').on('keyup','#new-example', function(e){
    console.log(e.keyCode);
    if(e.keyCode == 13){
        var parent_index = parseInt($(this).attr('parent-index'));
        addExample(parent_index);
    }
});

$('body').on('click','#example-add-row', function(){
    var parent_index = parseInt($(this).attr('parent-index'));
    addExample(parent_index);
});

$('body').on('click','.example-del-row', function(){
    var parent_index = parseInt($(this).attr('parent-index'));
    var index = parseInt($(this).attr('index'));
    nlu_details.intent.intents[parent_index].examples.splice(index, 1); 
});

function addExample(parent_index){
    if($('#new-example').val() != ''){
        nlu_details.intent.intents[parent_index].examples.push({
            'label':$('#new-example').val(),
            'id':generateID()
        });
        document.getElementById("new-example").value = '';
        processHTML('raw_input', false);
        saveFlow();
    }
}

/************** NEW Intent For Intents **************/
$('body').on('click','#intent-add-row', function(){
    var new_index = nlu_details.intent.intents.length + 1;
    nlu_details.intent.details = {
        "name":"New Intent",
        "examples":[],
        "parent_index":new_index
    };
    nlu_details.intent.intents.push(nlu_details.intent.details);
    setTimeout(function(){
        var nlu_rows = document.getElementsByClassName("intent-row");
        for(var i = 0; i<nlu_rows.length; i++){
            $(nlu_rows[i]).removeClass('active');
            if(i == nlu_rows.length-1){
                $(nlu_rows[i]).trigger( "click" );
            }
        }
        var tied_form_output = document.getElementsByClassName("tied-form-output");
        for(var i = 0; i<tied_form_output.length; i++){
            $(tied_form_output[i]).trigger('click');
        }
        saveFlow();
    },100)
});
// Trigger action when the contexmenu is about to be shown
var curr_holder_index;
var curr_row_index;

var left_pos;
var top_pos;
var use_click = false;
$('#vf-canvas-container').bind("contextmenu", function (event) {
    console.log(event);
    var class_name = event['target']['className'];
    var id_name = event['target']['id'];
    console.log(id_name);
    if(class_name == 'line '){
        curr_holder_index = event['target']['attributes']['holder-index']['value'];
        curr_row_index = event['target']['attributes']['row-index']['value'];
        curr_choice_index = event['target']['attributes']['choice-index']['value'];
        console.log('Right Clicked');
        
        // Avoid the real one
        event.preventDefault();
        
        // Show contextmenu
        $("#line-edit-menu").finish().toggle(100).
        
        // In the right position (the mouse)
        css({
            top: event.pageY + "px",
            left: event.pageX + "px"
        });
    }
    else if(class_name == 'speech-item'){
        curr_holder_index = event['target']['attributes']['holder-index']['value'];
        curr_row_index = event['target']['attributes']['row-index']['value'];
        console.log(curr_holder_index);
        console.log(curr_row_index);
        console.log('Right Clicked');
        
        // Avoid the real one
        event.preventDefault();
        
        // Show contextmenu
        $("#convo-item-menu").finish().toggle(100).
        
        // In the right position (the mouse)
        css({
            top: event.pageY + "px",
            left: event.pageX + "px"
        });
    }
    else if(id_name == 'vf-canvas-container' || id_name == 'vf-canvas'){        
        // Avoid the real one
        event.preventDefault();
        
        // Show contextmenu
        $("#flow-menu").finish().toggle(100).
        
        // In the right position (the mouse)
        css({
            top: event.pageY + "px",
            left: event.pageX + "px"
        });
        top_pos = event.pageY + "px";
        left_pos = event.pageX + "px";
        use_click = true;
    }
});

// If the document is clicked somewhere
$(document).bind("mousedown", function (e) {
    
    // If the clicked element is not the menu
    if (!$(e.target).parents(".custom-menu").length > 0) {
        
        // Hide it
        $(".custom-menu").hide(100);
    }
});


// If the menu element is clicked
$(".custom-menu li").click(function(){
    var type= $(this).attr("data-type");
    var action= $(this).attr("data-action");
    console.log(type);
    console.log(action);
    if(action == 'delete'){
        if(type == 'line-item'){
            conversation['holders'][curr_holder_index]['items'][curr_row_index]['choices'][curr_choice_index]['anchor_from'] = null;
            conversation['holders'][curr_holder_index]['items'][curr_row_index]['choices'][curr_choice_index]['anchor_to'] = null;
            saveFlow();
        }
        else if(type == 'convo-item'){
            conversation['holders'][curr_holder_index]['items'].splice(curr_row_index, 1); 
            saveFlow();
        }
        getCoordinates();

        // Hide it AFTER the action was triggered
        $(".custom-menu").hide(100);
    }
    else if(action == 'color'){

    }
    else if(action == 'insert'){
        if(type == 'flow-menu'){
            var new_holder_id = generateID();
            var translate = String(document.getElementById('vf-canvas').style.transform).replace(/[^-\d.,]/g, '');
            var translates = translate.split(',');
            var new_left_pos = parseFloat(left_pos)-parseFloat(translates[0]);
            var new_top_pos = parseFloat(top_pos)-parseFloat(translates[1]);
            console.log(new_left_pos);
            console.log(new_top_pos);
            if(use_click){
                var new_holder = {
                    'id':new_holder_id,
                    'index':conversation['holders'].length,
                    'label':'New Block',
                    'items':[{
                            "holder_index":conversation['holders'].length,
                            "id":generateID(),
                            "index":0,
                            "label":"Speak",
                            "row_index":0,
                            "type":"speak"
                        },{
                        "choices":[],
                        "holder_index":conversation['holders'].length,
                        "id":generateID(),
                        "index":1,
                        "label":"Choice",
                        "row_index":1,
                        "type":"choice",
                        "unkown_intent":{
                            "anchor_from":null,
                            "anchor_to":null,
                            "id":generateID()
                        }
                    }],
                    'style':{
                        'left':new_left_pos,
                        'top':new_top_pos,
                        'position':'absolute'
                    }
                }
                conversation['holders'].push(new_holder);
                getCoordinates();
        
                // Hide it AFTER the action was triggered
                $(".custom-menu").hide(100);
                use_click = false;
                new_holder_id = '#holder-'+new_holder_id;
                setTimeout(function(){
                    $(new_holder_id).css({position: 'absolute',top: new_top_pos, left:new_left_pos});
                    var x = $(new_holder_id).offset().left;
                    var y = $(new_holder_id).offset().top;
                    console.log(x);
                    console.log(y);
                    $(new_holder_id).css({position: 'relative'});
                    $(new_holder_id).offset({ top: y, left: x }); 
                },100)
            }
        }
    }
});

function updateHolderCoords(){
    var convo_cards = document.getElementsByClassName("convo-card");
    for(var i = 0; i<convo_cards.length; i++){
        var holder_index = $(convo_cards[i]).attr("holder-index");
        var coords = {
            "left":$(convo_cards[i]).css('left'),
            "top":$(convo_cards[i]).css('top')
        }
        conversation['holders'][holder_index]['style'] = coords;
        //console.log(coords);
    }
    console.log(conversation['holders']);
}
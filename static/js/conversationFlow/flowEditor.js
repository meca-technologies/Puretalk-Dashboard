var drag_function = {
    start: function(event){
        //removeLines();
    },
    drag:function(event){
        updateHolderCoords(),
        getCoordinates()
    },
    stop:function(event){
        //getCoordinates();
    }
};

var curr_zoom = 100;
var connectors = [];

$(document).ready(function(){
    setTimeout(function(){
        var holders = document.getElementsByClassName("convo-card");
        for(var i = 0; i<holders.length; i++){
            $(holders[i]).draggable(drag_function);
        }
    }, 1000)
})

var curr_anchor;
var curr_anchor_holder;
var next_anchor;
var next_anchor_holder;

function linedraw(ax,ay,bx,by, zoom_offset, extra_class = '', holder_index, row_index, choice_index){
    ax+=3;
    bx-=3;
    // Create the position of the vector
    var u = [bx - ax, by - ay];

    //Get tanθ
    var tanDeg = u[1] / u[0];

    //Get tan^-1
    var invTanDeg = Math.atan(tanDeg);

    //Convert radians to degrees
    var radsToDegs=invTanDeg*180/Math.PI;
    var degrees = radsToDegs;

    //Determine the quadrant you are in
    if(ax < bx && ay < by){
        degrees = radsToDegs - 90;
    }
    else if(ax > bx && ay < by){
        degrees = radsToDegs + 90;
    }
    else if(ax > bx && ay > by){
        degrees = radsToDegs + 90;
    }
    else if(ax < bx && ay > by){
        degrees = radsToDegs - 90;
    }
    else if(ax == bx && ay < by){
        degrees = 0;
    }
    else if(ax == bx && ay > by){
        degrees = 180;
    }
    else if(ax < bx && ay == by){
        degrees = 270;
    }
    else if(ax > bx && ay == by){
        degrees = 90;
    }

    //Get the magnitude
    var length = Math.sqrt((u[0]*u[0]) + (u[1] * u[1]));

    //Draw the line
    document.getElementById("line-body").innerHTML += "<div class='line "+extra_class+"' holder-index='"+holder_index+"' row-index='"+row_index+"' choice-index='"+choice_index+"' style='height:" + length + "px;width:1px;background-color:#616dff;position:absolute;top:" + (ay) + "px;left:" + (ax) + "px;transform:rotate(" + degrees + "deg);-ms-transform:rotate(" + degrees + "deg);transform-origin:0% 0%;-moz-transform:rotate(" + degrees + "deg);-moz-transform-origin:0% 0%;-webkit-transform:rotate(" + degrees  + "deg);-webkit-transform-origin:0% 0%;-o-transform:rotate(" + degrees + "deg);-o-transform-origin:0% 0%;'><div class='line-header' style='width: 10px;height: 10px;background-color: #616dff; position: relative; left: -6px; top: -10px; border-radius: 10px;'></div><div class='line-header' style='width: 10px;height: 10px;background-color: #616dff; position: relative; top: "+String(length-10)+"px;left: -5px; border-radius: 10px;'></div></div>"
}

function removeLines(class_name = 'line'){
    var lines = document.getElementsByClassName(class_name);
    for(var i = lines.length-1; i>=0; i--){
        lines[i].remove();
    }
}

function getCoordinates(){
    $('body').css('cursor', 'grabbing');
    removeLines();
    connectors = [];
    for(var i = 0; i<conversation['holders'].length; i++){
        for(var j = 0; j<conversation['holders'][i]['items'].length; j++){
            if(conversation['holders'][i]['items'][j]['type'] == 'choice'){
                for(var x = 0; x<conversation['holders'][i]['items'][j]['choices'].length; x++){
                    var anchor_from = conversation.holders[i].items[j].choices[x].anchor_from;
                    var anchor_to = conversation.holders[i].items[j].choices[x].anchor_to;
                    if(anchor_from && anchor_to){
                        console.log($(anchor_from).offset())
                        console.log($(anchor_to).offset())
                        if($(anchor_from).offset() !== undefined  && $(anchor_to).offset() !== undefined){
                            connectors.push({
                                'from':$(anchor_from),
                                'to':$(anchor_to),
                                'holder_index':i,
                                'row_index':j,
                                'choice_index':x,
                            })
                        }
                        else{
                            conversation.holders[i].items[j].choices[x].anchor_to = null;
                        }
                    }
                }
            }
        }
    }
    for(var i = 0; i<connectors.length; i++){
        //Calculate the translate offset
        var translate = String(document.getElementById('vf-canvas').style.transform).replace(/[^-\d.,]/g, '');
        var translates = translate.split(',');
        
        var curr_x_offset = 0;
        var curr_y_offset = 0;
        
        var curr_x = parseFloat(translates[0]);
        var curr_y = parseFloat(translates[1]);
        if(curr_x != 0){
            curr_x_offset = curr_x;
        }
        if(curr_y != 0){
            curr_y_offset = curr_y;
        }
        
        var zoom_offset = 1;
        
        document.getElementById('vf-canvas').style.transform = curr_trans + ' scale(1)';
        var coordOne = connectors[i]['from'].offset();
        //console.log(coordOne);
        var x1 = Math.round(coordOne.left + (connectors[i]['from'].width()/2) - curr_x_offset) * zoom_offset;
        var y1 = Math.round(coordOne.top + (connectors[i]['from'].height()/2) - curr_y_offset) * zoom_offset;
        var coordTwo = connectors[i]['to'].offset();
        var x2 = Math.round(coordTwo.left + (connectors[i]['to'].width()/2) - curr_x_offset) * zoom_offset;
        var y2 = Math.round(coordTwo.top + (connectors[i]['to'].height()/2) - curr_y_offset) * zoom_offset;
        document.getElementById('vf-canvas').style.transform = curr_trans + ' ' + curr_scale;

        linedraw(x1,y1,x2,y2, zoom_offset, '', connectors[i]['holder_index'], connectors[i]['row_index'], connectors[i]['choice_index']);
    }
}

function getCoordinatesMouse(mouse_event){
    //console.log(mouse_event.offset());
    removeLines('cursor_line');
    var translate = String(document.getElementById('vf-canvas').style.transform).replace(/[^-\d.,]/g, '');
    var translates = translate.split(',');
    
    var curr_x_offset = 0;
    var curr_y_offset = 0;
    
    var curr_x = parseFloat(translates[0]);
    var curr_y = parseFloat(translates[1]);
    if(curr_x != 0){
        curr_x_offset = curr_x;
    }
    if(curr_y != 0){
        curr_y_offset = curr_y;
    }
    
    var zoom_offset = 1;
    
    document.getElementById('vf-canvas').style.transform = curr_trans + ' scale(1)';
    var coordOne = $(curr_anchor).offset();
    var x1 = Math.round(coordOne.left + ($(curr_anchor).width()/2) - curr_x_offset) * zoom_offset;
    var y1 = Math.round(coordOne.top + ($(curr_anchor).height()/2) - curr_y_offset) * zoom_offset;
    var coordTwo = {
        'left':mouse_event['screenX'],
        'top':mouse_event['screenY']-60
    }
    var x2 = Math.round(coordTwo.left - curr_x_offset) * zoom_offset;
    var y2 = Math.round(coordTwo.top - curr_y_offset) * zoom_offset;
    document.getElementById('vf-canvas').style.transform = curr_trans + ' ' + curr_scale;

    linedraw(x1,y1,x2,y2, zoom_offset, 'cursor_line');
}

$('body').on('mousedown','.anchor-center', function(){
    var holders = document.getElementsByClassName("convo-card");
    for(var i = 0; i<holders.length; i++){
        $(holders[i]).draggable('destroy');
    }
    curr_anchor = $(this).attr('id');
    curr_anchor = '#'+curr_anchor;
    console.log(curr_anchor);
    console.log($(curr_anchor));
    console.log($(curr_anchor).parent());
    console.log($(curr_anchor).parent().parent());
    console.log($(curr_anchor).parent().parent().parent());
    $('body').css('cursor', 'copy');
    var anchor_body_ends = document.getElementsByClassName('anchor-body-end');
    console.log(anchor_body_ends);
    for(var i = 0; i<anchor_body_ends.length; i++){
            anchor_body_ends[i].style.visibility = '';
    }
    var lines = document.getElementsByClassName("line");
    for(var i = 0; i<lines.length; i++){
        $(lines[i]).css( 'pointer-events', 'none' );
    }
    var lines = document.getElementsByClassName("line-headers");
    for(var i = 0; i<lines.length; i++){
        $(lines[i]).css( 'pointer-events', 'none' );
    }
});

$('body').on('mouseup','.anchor-end', function(){
    if(curr_anchor){
        next_anchor = $(this).attr('id');
        next_anchor = '#'+next_anchor;
        console.log(next_anchor);
        //if($(curr_anchor).attr('id') != $(next_anchor).attr('id')){
        console.log('attach');

        var holder_index = $(curr_anchor).attr('holder-index');
        var row_index = $(curr_anchor).attr('row-index');
        var choice_index = $(curr_anchor).attr('choice-index');
        console.log(holder_index);
        console.log(row_index);
        console.log(choice_index);
        console.log($(curr_anchor));
        console.log($(next_anchor));
        conversation['holders'][holder_index]['items'][row_index].choices[choice_index]['anchor_from'] = curr_anchor;
        conversation['holders'][holder_index]['items'][row_index].choices[choice_index]['anchor_to'] = next_anchor;
        console.log(conversation);
        getCoordinates();
        $('body').css('cursor', 'inherit');
        var anchor_body_ends = document.getElementsByClassName('anchor-body-end');
        console.log(anchor_body_ends);
        for(var i = 0; i<anchor_body_ends.length; i++){
            anchor_body_ends[i].style.visibility = 'hidden';
        }
    //}
    }
    var lines = document.getElementsByClassName("line");
    for(var i = 0; i<lines.length; i++){
        $(lines[i]).css( 'pointer-events', '' );
    }
    var lines = document.getElementsByClassName("line-headers");
    for(var i = 0; i<lines.length; i++){
        $(lines[i]).css( 'pointer-events', '' );
    }
});

$('body').on('click','.row-item-up',function(){
    var holder_index = $(this).attr('holder-index');
    var row_index = parseInt($(this).attr('row-index'));
    var choice_index = $(curr_anchor).attr('choice-index');
    if(row_index > 0){
    console.log(row_index);
        var next_index = parseInt(row_index) - 1;
        console.log(conversation.holders[holder_index].items[row_index]);
        console.log(conversation.holders[holder_index].items[next_index]);
        var temp_item = {
            'id':conversation.holders[holder_index].items[row_index]['id'],
            'index':conversation.holders[holder_index].items[row_index]['index'],
            'label':conversation.holders[holder_index].items[row_index]['label'],
            'type':conversation.holders[holder_index].items[row_index]['type']
        }

        one_anchor_from = conversation.holders[holder_index].items[row_index]['anchor_from'];
        one_anchor_to = conversation.holders[holder_index].items[row_index]['anchor_to'];
        console.log([one_anchor_from, one_anchor_to]);

        two_anchor_from = conversation.holders[holder_index].items[next_index]['anchor_from'];
        two_anchor_to = conversation.holders[holder_index].items[next_index]['anchor_to'];
        console.log([two_anchor_from, two_anchor_to]);

        conversation.holders[holder_index].items[row_index]['id'] = conversation.holders[holder_index].items[next_index]['id'];
        conversation.holders[holder_index].items[row_index]['index'] = conversation.holders[holder_index].items[next_index]['index'];
        conversation.holders[holder_index].items[row_index]['label'] = conversation.holders[holder_index].items[next_index]['label'];
        conversation.holders[holder_index].items[row_index]['type'] = conversation.holders[holder_index].items[next_index]['type'];
        
        conversation.holders[holder_index].items[next_index]['id'] = temp_item['id'];
        conversation.holders[holder_index].items[next_index]['index'] = temp_item['index'];
        conversation.holders[holder_index].items[next_index]['label'] = temp_item['label'];
        conversation.holders[holder_index].items[next_index]['type'] = temp_item['type'];
    }
})
        
$('body').on('click','.row-item-down',function(){
    var holder_index = $(this).attr('holder-index');
    var row_index = parseInt($(this).attr('row-index'));
    var choice_index = $(curr_anchor).attr('choice-index');
    console.log(row_index);
    var next_index = parseInt(row_index) + 1;
    console.log(next_index);
    console.log(conversation.holders[holder_index].items.length);
    if(next_index < conversation.holders[holder_index].items.length-1){
        console.log(conversation.holders[holder_index].items[row_index]);
        console.log(conversation.holders[holder_index].items[next_index]);
        var temp_item = {
            'id':conversation.holders[holder_index].items[row_index]['id'],
            'index':conversation.holders[holder_index].items[row_index]['index'],
            'label':conversation.holders[holder_index].items[row_index]['label'],
            'type':conversation.holders[holder_index].items[row_index]['type']
        }

        one_anchor_from = conversation.holders[holder_index].items[row_index]['anchor_from'];
        one_anchor_to = conversation.holders[holder_index].items[row_index]['anchor_to'];
        console.log([one_anchor_from, one_anchor_to]);

        two_anchor_from = conversation.holders[holder_index].items[next_index]['anchor_from'];
        two_anchor_to = conversation.holders[holder_index].items[next_index]['anchor_to'];
        console.log([two_anchor_from, two_anchor_to]);

        conversation.holders[holder_index].items[row_index]['id'] = conversation.holders[holder_index].items[next_index]['id'];
        conversation.holders[holder_index].items[row_index]['index'] = conversation.holders[holder_index].items[next_index]['index'];
        conversation.holders[holder_index].items[row_index]['label'] = conversation.holders[holder_index].items[next_index]['label'];
        conversation.holders[holder_index].items[row_index]['type'] = conversation.holders[holder_index].items[next_index]['type'];
        
        conversation.holders[holder_index].items[next_index]['id'] = temp_item['id'];
        conversation.holders[holder_index].items[next_index]['index'] = temp_item['index'];
        conversation.holders[holder_index].items[next_index]['label'] = temp_item['label'];
        conversation.holders[holder_index].items[next_index]['type'] = temp_item['type'];
    }
    else{
        console.log('Do Nothing');
    }
})

var curr_line;
$('body').on('mouseenter','.line', function(){
    curr_line = this;
    $(curr_line).css('width', '3px');
    $(curr_line).css('background-color', 'red');
    $('body').css('cursor', 'pointer');
});

$('body').on('mouseleave','.line', function(){
    curr_line = this;
    $(curr_line).css('width', '1px');
    $(curr_line).css('background-color', '#616dff');
    $('body').css('cursor', 'initial');
});

$('body').on('click','.add-item', function(){
    var holder_index = $(this).attr('index');
    var new_item = {
        'id':generateID(),
        'index':0,
        'label':'Test Sub Label 1',
        'type':'speak',
    }
    conversation['holders'][holder_index]['items'].push(new_item);
});

var clicking = false;
var mouse_start = {
    'left':0,
    'top':0
};

var curr_trans = conversation.canvas_translate;
var curr_scale = 'scale(1)';
document.getElementById('vf-canvas').style.transform = curr_trans + ' ' + curr_scale;
document.getElementById("vf-canvas-container").onwheel = function(event){
    if(event['deltaY'] > 0 && curr_zoom > 50){
        curr_zoom -= 5;
    }
    else if(event['deltaY'] < 0 && curr_zoom < 150){
        curr_zoom += 5;
    }
    var new_zoom = curr_zoom/100;
    curr_scale = 'scale('+String(new_zoom)+')';
    canvas_details.zoom = String(curr_zoom)+'%'
    document.getElementById('vf-canvas').style.transform = curr_trans + ' ' + curr_scale;
};

$("#vf-canvas-container").mousedown(function(event){
    console.log(event);
    if(event['target'] == $("#vf-canvas-container")[0] || event['target'] == $("#vf-canvas")[0]){
        //console.log('StartX:' + String(event['pageX']));
        //console.log('StartY:' + String(event['pageY']));
        mouse_start['left'] = event['pageX'];
        mouse_start['top'] = event['pageY'];
        var translate = String(document.getElementById('vf-canvas').style.transform).replace(/[^-\d.,]/g, '');
        var translates = translate.split(',');
        //console.log('DivStartX:' + String(translates[0]));
        //console.log('DivStartY:' + String(translates[1]));
        clicking = true;
    }
});

$(window).mousemove(function(event){
    if(curr_anchor){
        getCoordinatesMouse(event);
    }
    if(clicking){
        var translate = String(document.getElementById('vf-canvas').style.transform).replace(/[^-\d.,]/g, '');
        var translates = translate.split(',');
        var curr_x = parseFloat(translates[0]);
        var curr_y = parseFloat(translates[1]);
        var diff_x = mouse_start['left'] - event['pageX'];
        var diff_y = mouse_start['top'] - event['pageY'];
        //console.log(diff_x);
        //console.log(diff_y);
        //console.log('DiffX:' + String(diff_x));
        //console.log('DiffY:' + String(diff_y));
        var new_x = parseFloat(translates[0]) - diff_x;
        var new_y = parseFloat(translates[1]) - diff_y;
        //console.log(new_x);
        //console.log(new_y);
        //console.log('NewX:' + String(new_x));
        //console.log('NewY:' + String(new_y));
        //console.log('translate('+String(new_x)+'px, '+String(new_y)+'px)');
        curr_trans = 'translate('+String(new_x)+'px, '+String(new_y)+'px)';
        conversation.canvas_translate = curr_trans;
        document.getElementById('vf-canvas').style.transform = curr_trans + ' ' + curr_scale;
        //console.log('------------------------------------------------------------------------------------');
        mouse_start['left'] = event['pageX'];
        mouse_start['top'] = event['pageY'];
        $('body').css('cursor', 'grabbing');
    }
});

$(window).mouseup(function(event){
    curr_anchor = null;
    next_anchor = null;
    clicking = false;
    mouse_start = {
        'left':0,
        'top':0
    };
    $('body').css('cursor', 'inherit');
    var holders = document.getElementsByClassName("convo-card");
    for(var i = 0; i<holders.length; i++){
        $(holders[i]).draggable(drag_function);
    }
    removeLines('cursor_line');
});
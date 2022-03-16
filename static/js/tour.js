var steps = [];
var step = 0;

function intro(index){
    if(index > 0){
        if(steps[index-1]['action'] != '#'){
            window.location.href = steps[index-1]['action'];
        }
    }
    document.getElementById("tour-bg").style.display = '';
    document.getElementById("carver").style.display = 'none';
    document.getElementById("carver-tooltip").style.display = '';

    for(var i = 0; i<steps.length; i++){
        try{
            document.getElementById(steps[i]['id']).style.zIndex = steps[i]['zIndex'];
            document.getElementById(steps[i]['id']).style.position = '';
        }catch(error){}
    }

    if(index === undefined){
        index = step;
    }
    
    var selects = document.getElementsByClassName("gal-sel");
    for(var i = 0; i<selects.length; i++){
        $(selects[i]).removeClass("active");
    }
    $(selects[index]).addClass("active");

    var step_div = document.getElementById(steps[index]['id']);
    var step_box = step_div.getBoundingClientRect();
    var left = step_box.left;
    var top = step_box.top + window.scrollY;
    var width = step_div.offsetWidth;
    var height = step_div.offsetHeight;

    
    $( document.getElementById("carver") ).animate({
        width:width+'px',
        height:height+'px',
        left:left+'px',
        top:top+'px'
    }, 500, function(){
        document.getElementById("carver").style.zIndex = 9999;
        document.getElementById(steps[index]['id']).style.zIndex = 10000;
        document.getElementById("carver-tooltip").style.zIndex = 10000;
        document.getElementById("carver").style.display = '';
    });
    document.getElementById(steps[index]['id']).style.position = 'relative';

    $( document.getElementById("carver-tooltip") ).animate({
        width:width+'px',
        height:height+'px',
        left:left+'px',
        top:parseInt(height+top+10)+'px'
    }, 500);

    document.getElementById("carver-tooltip-text").innerHTML = steps[index]['text'];

    
    $('html, body').animate({
        scrollTop: $(step_div).offset().top-20
    }, 500);

}

function initializeIntro(){
    setTimeout(function(){
        var htmlContent = '';
        for(var i = 0; i<steps.length; i++){
            console.log(steps[i]['id']);
            steps[i]['zIndex'] = document.getElementById(steps[i]['id']).style.zIndex;
            if(i == 0){
                htmlContent += '<div class="m-1 gal-sel active" index="'+i+'"></div>';
            }
            else{
                htmlContent += '<div class="m-1 gal-sel" index="'+i+'"></div>';
            }
        }
        console.log(steps);
        document.getElementById("gal-sel-holder").innerHTML = htmlContent;
        intro();
    }, 2000);
}

$('body').on('click','.gal-sel', function(){
    step = parseInt($(this).attr("index"));
    intro();
})

$("#prev").click(function(){
    if(step>0){
        step-=1;
        intro();
    }
    else{
        if(steps[step]['prev'] != '#'){
            window.location.href = steps[step]['prev'];
        }
    }
})

$("#next").click(function(){
    if(step<steps.length-1){
        step+=1;
        intro();
    }
    else{
        if(steps[step]['next'] != '#'){
            window.location.href = steps[step]['next'];
        }
        else{
            endIntro();
        }
    }
})

$("#close-intro").click(function(){
    endIntro();
})

function endIntro(){
    document.getElementById("tour-bg").style.display = 'none';
    document.getElementById("carver").style.display = 'none';
    document.getElementById("carver-tooltip").style.display = 'none';

    for(var i = 0; i<steps.length; i++){
        try{
            document.getElementById(steps[i]['id']).style.zIndex = steps[i]['zIndex'];
            document.getElementById(steps[i]['id']).style.position = '';
        }catch(error){}
    }
    postToAPI('/api/v1/users-tour', {}, 'POST', 'doNothing');
}
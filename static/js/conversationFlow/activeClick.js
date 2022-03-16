var curr_active_item;
var hadClass = true;
$('body').on('mousedown','.active-click', function(){
    console.log('Active Click');
    if(curr_active_item){
        if(!hadClass){
            $(curr_active_item).removeClass('border');
        }
        $(curr_active_item).removeClass('border-primary');
    }
    curr_active_item = this;
    if(!$(curr_active_item).hasClass('border')){
        hadClass = false;
        $(curr_active_item).addClass('border');
    }
    else{
        hadClass = true;
    }
    $(curr_active_item).addClass('border-primary');
})
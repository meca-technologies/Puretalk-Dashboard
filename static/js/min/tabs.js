$(document).ready(function(){
    $('.setting-link').click(function(){
        if(!($(this).hasClass('active'))){
            var myTabGroup = $(this).attr('tab-group');
            var attr = '[tab-group="'+myTabGroup+'"]';
            tabGroups = $(attr);
            for(var i = 0; i<tabGroups.length; i++){
                $(tabGroups[i]).removeClass('active');
            }
            
            var attr = '[tab-parent="'+myTabGroup+'"]';
            tabGroups = $(attr);
            for(var i = 0; i<tabGroups.length; i++){
                $(tabGroups[i]).hide(300);
            }
    
            var tabTarget = $(this).attr('tab-target');
            var tabID = '#'+tabTarget;
            console.log(tabID);
            $(tabID).show(300);
    
            $(this).addClass('active');
        }
    })
});
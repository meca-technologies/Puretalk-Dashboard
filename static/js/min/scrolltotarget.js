var last_target = ''; 
$(".scroll-to-api").click(function() {
    var target_id = $(this).attr('data-target');
    if(last_target != target_id){
        last_target = target_id;
        var target = document.getElementById(target_id);
        var scrollers = $(".scroll-to-api");
        for(var i = 0; i<scrollers.length; i++){
            $(scrollers[i]).removeClass("active");
        }
        $(this).addClass("active");
        
        $('#api-body').animate({
                scrollTop: $(target).offset().top
        }, 500);
    }
});
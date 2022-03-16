$('body').on('click','[data-toggle="modal"]', function(){
    var modal_id = $(this).attr("data-target");
    console.log(modal_id);
    $(modal_id).fadeIn(200);
});
$('body').on('mousedown','.custom-modal', function(e){
    if($(e.target).hasClass('custom-modal')){
        console.log(this.style.display);
        $(this).fadeOut(200);
    }
});

$('body').on('click','[data-dismiss="modal"]', function(){
    var modal_id = $(this).attr("data-target");
    console.log(modal_id);
    $(modal_id).fadeOut(200);
});
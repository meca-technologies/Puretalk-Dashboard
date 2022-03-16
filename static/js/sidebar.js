// this script was built for us to do custom modals that are like a slide bar
// this works by having a toggle object with the class "sidebar-toggle" and
// setting the target to toggle in the href attr
// the target id is the id attr we give to the modal itself
// This is to store the heirarchy of open modals
var modalName = [];

// if we click on a trigger
$('body').on('click','.sidebar-toggle', function(){
    console.log('TOGGLE ME PLEASE')
    // we store this because we will need to reference it later
    var _this = this;

    // add the new modal to the heirarchy and get its name
    modalName.push($(this).attr('href'));
    var thisModalName = modalName[modalName.length-1];
    console.log(thisModalName)

    var clickMe = setInterval(function(){
        if($(thisModalName).css( "display" ) != 'block'){
            $(thisModalName).css( "display", "block" );
            $(thisModalName).show(0, function(){
        
                // grab the side bar we will be animating
                var sidebar = $(this).find( ".sidebar-content" );
                var trans = $(this).find( ".sidebar-transparent" );
                trans[0].style.display = 'none';
                console.log($($(this).find( ".sidebar-content" )))
        
                var width = '+='+sidebar[0].offsetWidth+'px';
                // animate sliding in from the right
                $( sidebar[0] ).animate({
                    right:width
                }, 500, function(){
                    // this is just in case the slider breaks 
                    // and doesn't slide completely into position
                    sidebar[0].style.right = '0px';
                
                    $(trans[0]).fadeIn(500);
                });
            });
        }
        else{
            clearInterval(clickMe);
        }
    }, 100)
});

// capture all click events to close the modal when needed
$('body').on('click','.sidebar-transparent', function(){
    if(modalName.length != 0){
        // grab the top modal in the heirarchy 
        // and pop it since we are closing it
        var thisModalName = modalName[modalName.length-1];
        modalName.pop();

        // store the modal we popped as we will be referencing later
        var _this = $(thisModalName);

        // grab the side bar we will be animating
        var sidebar = $(_this).find( ".sidebar-content" );
        var trans = $(_this).find( ".sidebar-transparent" );
                
        $(trans[0]).fadeOut(100);

        var widthAnim = '-='+sidebar[0].offsetWidth+'px';
        var width = '-'+sidebar[0].offsetWidth+'px';

        // animate sliding offscreen
        $( sidebar[0] ).animate({
            right:widthAnim
        }, 500, function(){
            // this is just in case the slider breaks 
            // and doesn't slide completely into position
            sidebar[0].style.right = width;
            $(_this).hide(0);
        });
    }
});
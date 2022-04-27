var window_location = getURLParam('location');
if(window_location == 'project-details'){
    window_location = 'projects'; 
    window.history.replaceState('', '', updateURLParameter(window.location.href, "location", window_location));
}
var project_id = getURLParam('project');
if(!window_location || window_location == null){
    window_location = default_location;
    var newURL = updateURLParameter(window.location.href, 'location', window_location);
    window.history.replaceState('', '', updateURLParameter(window.location.href, "location", window_location));
}
changeLocation(window_location);
$('body').on('click','.location-change', function(){
    window_location = $(this).attr("window-location");
    window.history.replaceState('', '', updateURLParameters('location', window_location));
    changeLocation(window_location);
})

$('body').on('click','.project-change', function(){
    project_id = $(this).attr("project-id");
    var project_index = 0;
    for(var i = 0; i<projects['projects'].length; i++){
        if(projects['projects'][i]['project_number'] == project_id){
            project_index = i;
        }
    }
    console.log(project_index);
    console.log(projects['projects'][project_index]);
    projectDetails['details'] = projects['projects'][project_index];
})

var data_target;
function changeLocation(location){
    var content_doms = document.getElementsByClassName("content");
    for(var i = 0; i<content_doms.length; i++){
        $(content_doms[i]).removeClass('active')
    }
    //document.getElementById(location).classList.add("active");
    $('#'+location).addClass('active');
}

$(document).bind("click", function (e) {
    if(!$(e.target).hasClass('dropdown-custom')){
        if(data_target != $(e.target.offsetParent).attr('id')){
            $('#'+data_target).removeClass('active');
            data_target = null;
        }
    }
});

$('body').on('click','.dropdown-custom', function(){
    data_target = $(this).attr("data-target");
    $('#'+data_target).addClass('active');
});
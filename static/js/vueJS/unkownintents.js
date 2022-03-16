var unkownIntents = new Vue({
    delimiters: ['[[', ']]'],
    el: '#unkown-intents',
    data: {
        unkownIntents:[]
    }
})
var leadIntentDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#unknown-intent-edit',
    data: {
        details:{
            call_log:{}
        }
    }
})

var intent_table;

$(".lead-campaigns").change(function(){
    if($(this).val() != ''){
        getUnkownIntents();
    }
});

function getUnkownIntents(){
    document.getElementById('unkown-intents-loading').style.display = '';
    document.getElementById('unkown-intents').style.display = 'none';
    var url = '/api/v1/unkown_intents?campaignid='+$("#campaign-body").val();
    var jqxhr = $.get( url, function(data) {
        console.log(data);
        unkownIntents.unkownIntents = data;
        try{
            intent_table.destroy();
        }catch(error){}
    }).always(function(){
        try{
            setTimeout(function(){
                intent_table = $('#unkown-intents').DataTable({
                    "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
                    "language": {
                        "paginate": {
                            "previous": "<<",
                            "next": ">>"
                        }
                    },
                    initComplete: function() {
                        $(this.api().table().container()).find('input[type="search"]').parent().wrap('<form>').parent().attr('autocomplete','off').css('overflow','hidden').css('margin','auto');
                    }   
                });
            }, 1000)
            document.getElementById('unkown-intents-loading').style.display = 'none';
            document.getElementById('unkown-intents').style.display = '';
        }catch(error){}
    });
}

$('body').on('click','.unknown-intent-edit', function(){
    var url = '/api/v1/leads?campaignid='+$(this).attr('campaign-id')+'&leadid='+$(this).attr('lead-id')+'&callid='+$(this).attr('call-id');
    try{
        document.getElementById("unknown-intent-edit-body").style.display = "none";
        document.getElementById("unknown-intent-edit-loading").style.display = "";
    }catch(error){}
    console.log(url);
    var jqxhr = $.get( url, function(data) {
        console.log(data[0]);
        leadIntentDetails.details = data[0];
        document.getElementById("unknown-intent-edit-body").style.display = "";
        document.getElementById("unknown-intent-edit-loading").style.display = "none";
        setTimeout(function(){
            document.getElementById("recording-audio").load();
        },1000)
    })
});

$('body').on('click','.unknown-intent-check', function(){
    var update_data = {
        'id':$(this).attr('intent-id'),
        'checked':true
    }
    console.log(update_data);
    var url = '/api/v1/unkown_intents';
    postToAPI(url, update_data, 'PUT', 'getUnkownIntents');
})
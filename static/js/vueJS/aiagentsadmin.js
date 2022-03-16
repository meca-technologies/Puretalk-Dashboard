var aiAgentsAdmin = new Vue({
    delimiters: ['[[', ']]'],
    el: '#ai-agent-admin-body',
    data: {
        aiAgentsAdmin:[]
    }
})

function updateAIAgentsAdmin(){
    var jqxhr = $.get( '/api/v1/ai-agents?limit=2000', function(data) {
        console.log(data);
        aiAgentsAdmin.aiAgentsAdmin = data;
    })
}

updateAIAgentsAdmin();
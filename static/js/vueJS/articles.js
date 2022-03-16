var articles = new Vue({
    delimiters: ['[[', ']]'],
    el: '#article-body',
    data: {
        articles:[]
    }
})
var articleDetails = new Vue({
    delimiters: ['[[', ']]'],
    el: '#article-edit',
    data: {
        details:{}
    }
})

function updateArticles(){
    var jqxhr = $.get( '/api/v1/articles?limit=2000', function(data) {
        console.log(data);
        articles.articles = data;
    })
}

$('body').on('click','.article-edit', function(){
    var url = '/api/v1/articles?articleid='+$(this).attr('article-id');
    var jqxhr = $.get( url, function(data) {
        articleDetails.details = data[0];
        $('#summernote').summernote("code", articleDetails.details.body);
    });
});

$("#add-article").click(function(){
    var title = $("#add-article-title").val();
    var split_title = String(title).toLocaleLowerCase().split(' ');
    var slug = split_title.join('-');
    var postData = {
        "title":title,
        "slug":slug,
        "body":$('#summernote-new').val()
    }
    console.log(postData);
});

$("#edit-article").click(function(){
    var title = $("#edit-article-title").val();
    var split_title = String(title).toLocaleLowerCase().split(' ');
    var slug = split_title.join('-');
    var postData = {
        "title":title,
        "slug":slug,
        "body":$('#summernote').val()
    }
    console.log(postData);
});

updateArticles();
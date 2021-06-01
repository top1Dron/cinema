function deleteMovie(button){
    if(confirm('Вы уверены, что хотите удалить этот фильм из базы данных?')){
        deleteUrl = $(button).attr("delete-url");
        $.ajax({
            url: deleteUrl,
            type: 'DELETE',
            data: {},
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
            success: function(resp){
                $(button).parent().parent().html("");
            }
        });
    }
}

function getCookie(name) {

    var matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ))
    return matches ? decodeURIComponent(matches[1]) : undefined
};
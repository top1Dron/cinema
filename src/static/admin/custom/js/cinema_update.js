$(document).ready(function(){
    $('#id_description_ru').summernote({
        height: '200px',
    });
    
    $('#id_description_uk').summernote({
        height: '200px',
    });

    $('#id_condition_ru').summernote({
        height: '200px',
    });
    
    $('#id_condition_uk').summernote({
        height: '200px',
    });

    $('#id_logo').change(function(event){
        if(typeof event.target.files[0] !== 'undefined'){
            $('#logo').attr("src", URL.createObjectURL(event.target.files[0]));
        }
        else {
            URL.revokeObjectURL($('#logo').attr("src"));
            $('#logo').attr("src", "/static/img/default-image.jpg")
        }
    });

    $('#id_banner').change(function(event){
        if(typeof event.target.files[0] !== 'undefined'){
            $('#banner').attr("src", URL.createObjectURL(event.target.files[0]));
        }
        else {
            URL.revokeObjectURL($('#banner').attr("src"));
            $('#banner').attr("src", "/static/img/default-image.jpg")
        }
    });

    $('.col-md-6', $('#images')).each(function(){
        var uploadButton = $(this).children('.card').children('.card-body').children('input')[0];
        onImageButtonUpload(uploadButton);
    });

    $('#add_more').click(function() {
        for(var ind=0; ind<4; ind++){
            var form_idx = $('#id_cinema_gallery-TOTAL_FORMS').val();
            $('#images').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
            var totalForms = parseInt(form_idx) + 1;
            $('#id_cinema_gallery-TOTAL_FORMS').val(totalForms);
            
            var imageColumn = $('#images').children('.col-md-6').last();
            var img = $(imageColumn).children('.card').children('img')[0];
            var image_id = img.getAttribute('id') + totalForms.toString();
            $(img).attr('id', image_id);
            var uploadButton = $(imageColumn).children('.card').children('.card-body').children('input')[0];
            onImageButtonUpload(uploadButton);
        }
    });
})

function onImageButtonUpload(uploadButton){
    $(uploadButton).change(function(event){
        var image_id = '#' + $(this).parent().parent().children('img')[0].getAttribute('id');
        if(typeof event.target.files[0] !== 'undefined'){
            $(image_id).attr("src", URL.createObjectURL(event.target.files[0]));
        }
        else {
            URL.revokeObjectURL($(image_id).attr("src"));
            if($(image_id).attr("image-start-src") == "..."){
                $(image_id).attr("src", "/static/img/default-image.jpg");
            }
            else{
                $(image_id).attr("src", $(image_id).attr("image-start-src"));
            }
        }
    });
}

function deleteImage(button, form_ind){

    var url = button.getAttribute('delete-url');
    if (url != null){
        $.ajax({
            url: url,
            type: 'DELETE',
            data: {},
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
            success: function(resp){
                $(`#id_cinema_gallery-${form_ind}-DELETE`).attr('checked', true);
                $(button).parent().parent().addClass("d-none");
            }
        });
    }
    else{
        $(button).parent().parent().remove();
    }
    $('#id_cinema_gallery-TOTAL_FORMS').val($('#id_cinema_gallery-TOTAL_FORMS').val() - 1);
}

function deleteHall(button){
    deleteUrl = $(button).attr("delete-url");
    $.ajax({
        url: deleteUrl,
        type: 'DELETE',
        data: {},
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        },
        success: function(resp){
            window.location.reload();
        }
    });
}

function getCookie(name) {

    var matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ))
    return matches ? decodeURIComponent(matches[1]) : undefined
};
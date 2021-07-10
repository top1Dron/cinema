$(document).ready(function(){
    $('#id_description_ru').summernote({
        height: '200px',
    });
    
    $('#id_description_uk').summernote({
        height: '200px',
    });

    $('.card.ms-2').matchHeight();

    $('#id_main_image').change(function(event){
        if(typeof event.target.files[0] !== 'undefined'){
            $('#main_image').attr("src", URL.createObjectURL(event.target.files[0]));
            $($(this).parent().children('.custom-file-label')[0]).html(event.target.files[0].name);
        }
        else {
            URL.revokeObjectURL($('#main_image').attr("src"));
            if($('#main_image').attr("image-start-src") == "..."){
                $('#main_image').attr("src", "/static/img/default-image.jpg");
            }
            else{
                $('#main_image').attr("src", $('#main_image').attr("image-start-src"));
            }
            $($(this).parent().children('.custom-file-label')[0]).html('Загрузите файл');
        }
    });
    
    $('.col-md-6', $('#images')).each(function(){
        var uploadButton = $(this).children('.card').children('.card-body').children('.form-group').children('.input-group').children('.custom-file').children('input')[0];
        onImageButtonUpload(uploadButton);
    });

    $('#add_more').click(function() {
        for(var ind=0; ind<4; ind++){
            var form_idx = $('#id_children_room_page-TOTAL_FORMS').val();
            $('#images').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
            var totalForms = parseInt(form_idx) + 1;
            $('#id_children_room_page-TOTAL_FORMS').val(totalForms);
            
            var imageColumn = $('#images').children('.col-md-6').last();
            var uploadButton = $(imageColumn).children('.card').children('.card-body').children('.form-group').children('.input-group').children('.custom-file').children('input')[0];
            onImageButtonUpload(uploadButton);
        }
    });
})

function onImageButtonUpload(uploadButton){
    $(uploadButton).change(function(event){
        var image_id = '#' + $(this).parent().parent().parent().parent().parent().children('img')[0].getAttribute('id');
        if(typeof event.target.files[0] !== 'undefined'){
            $(image_id).attr("src", URL.createObjectURL(event.target.files[0]));
            $($(this).parent().children('.custom-file-label')[0]).html(event.target.files[0].name);
        }
        else {
            URL.revokeObjectURL($(image_id).attr("src"));
            if($(image_id).attr("image-start-src") == "..."){
                $(image_id).attr("src", "/static/img/default-image.jpg");
            }
            else{
                $(image_id).attr("src", $(image_id).attr("image-start-src"));
            }
            $($(this).parent().children('.custom-file-label')[0]).html('Загрузите файл');
        }
        $('.card.ms-2').matchHeight();
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
                $(`#id_children_room_page-${form_ind}-DELETE`).attr('checked', true);
                $(button).parent().parent().addClass("d-none");
            }
        });
    }
    else{
        $(button).parent().parent().remove();
    }
    $('#id_children_room_page-TOTAL_FORMS').val($('#id_children_room_page-TOTAL_FORMS').val() - 1);
    $('.card.ms-2').matchHeight();      
}

function getCookie(name) {

    var matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ))
    return matches ? decodeURIComponent(matches[1]) : undefined
};
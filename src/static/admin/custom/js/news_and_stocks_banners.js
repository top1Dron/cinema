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

$('.col-md-6', $('#images')).each(function(){
    var uploadButton = $(this).children('.card').children('.card-body').children('.form-group').children('.input-group').children('.custom-file').children('input')[0];
    onImageButtonUpload(uploadButton);
});

$('#add_more').click(function() {
    for(var ind=0; ind<4; ind++){
        var form_idx = $('#id_news_and_stocks-TOTAL_FORMS').val();
        $('#images').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
        var totalForms = parseInt(form_idx) + 1;
        $('#id_news_and_stocks-TOTAL_FORMS').val(totalForms);
        
        var imageColumn = $('#images').children('.col-md-6').last();
        var uploadButton = $(imageColumn).children('.card').children('.card-body').children('.form-group').children('.input-group').children('.custom-file').children('input')[0];
        onImageButtonUpload(uploadButton);
    }
});

function add_images_to_formset(formset_id){
    var form_idx = $('#id_news_and_stocks-TOTAL_FORMS').val();
    $(`#${formset_id}`).append($(`#${formset_id}_empty_form`).html().replace(/__prefix__/g, form_idx));
    var totalForms = parseInt(form_idx) + 1;
    $('#id_news_and_stocks-TOTAL_FORMS').val(totalForms);
    
    var imageColumn = $(formset_id).children('.col-md-6').last();
    var img = $(imageColumn).children('.card').children('img')[0];
    var image_id = img.getAttribute('id') + totalForms.toString();
    $(img).attr('id', image_id);
    var uploadButton = $(imageColumn).children('.card').children('.card-body').children('.form-group').children('.input-group').children('.custom-file').children('input')[0];
    onImageButtonUpload(uploadButton);
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
                $(`#news_and_stocks-${form_ind}-DELETE`).attr('checked', true);
                $(button).parent().parent().addClass("d-none");
                $('.card.ms-2').matchHeight();
            }
        });
    }
    else{
        $(button).parent().parent().remove();
        $('.card.ms-2').matchHeight();
    }    
}

function getCookie(name) {

    var matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ))
    return matches ? decodeURIComponent(matches[1]) : undefined
};
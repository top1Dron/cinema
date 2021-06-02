$('#id_description_ru').summernote({
    height: '200px',
});

$('#id_description_uk').summernote({
    height: '200px',
});

$('#id_seo_description').summernote({
    height: '200px',
});



$('#id_poster').change(function(event){
    if(typeof event.target.files[0] !== 'undefined'){
        $('#main_poster').attr("src", URL.createObjectURL(event.target.files[0]));
    }
    else {
        URL.revokeObjectURL($('#main_poster').attr("src"));
        $('#main_poster').attr("src", "/static/img/default-image.jpg")
    }
});

$('.col-md-6', $('#images')).each(function(){
    // console.log($(this));
    var uploadButton = $(this).children('.card').children('.card-body').children('input')[0];
    onImageButtonUpload(uploadButton);
});

$('#add_more').click(function() {
    for(var ind=0; ind<4; ind++){
        var form_idx = $('#id_app-image-content_type-object_id-TOTAL_FORMS').val();
        $('#images').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
        var totalForms = parseInt(form_idx) + 1;
        $('#id_app-image-content_type-object_id-TOTAL_FORMS').val(totalForms);
        
        var imageColumn = $('#images').children('.col-md-6').last();
        var img = $(imageColumn).children('.card').children('img')[0];
        var image_id = img.getAttribute('id') + totalForms.toString();
        $(img).attr('id', image_id);
        var uploadButton = $(imageColumn).children('.card').children('.card-body').children('input')[0];
        onImageButtonUpload(uploadButton);
    }
});

function onImageButtonUpload(uploadButton){
    $(uploadButton).change(function(event){
        var image_id = '#' + $(this).parent().parent().children('img')[0].getAttribute('id');
        // console.log(image_id);
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

$(function () {
    
    $('#reservationdate').datetimepicker({
        format:'DD.MM.YYYY',
    });
});

$("input[data-bootstrap-switch]").each(function(){
    $(this).bootstrapSwitch('state', $(this).prop('checked'));
});

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
                $(button).parent().parent().html($('#empty_form').html().replace(/__prefix__/g, form_ind));
                var imageColumn = $('#images').children('.col-md-6').children('.col-md-6')[0];
                var img = $(imageColumn).children('.card').children('img')[0];
                var image_id = img.getAttribute('id') + form_ind.toString();
                $(img).attr('id', image_id);
                var uploadButton = $(imageColumn).children('.card').children('.card-body').children('input')[0];
                onImageButtonUpload(uploadButton);
            }
        });
    }
    else{
        $(button).parent().parent().remove();
    }    
}

function getCookie(name) {

    var matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ))
    return matches ? decodeURIComponent(matches[1]) : undefined
};
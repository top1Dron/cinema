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

    $('.card.ms-2').matchHeight();

    $('#id_logo').change(function(event){
        if(typeof event.target.files[0] !== 'undefined'){
            $('#logo').attr("src", URL.createObjectURL(event.target.files[0]));
            $($(this).parent().children('.custom-file-label')[0]).html(event.target.files[0].name);
        }
        else {
            URL.revokeObjectURL($('#logo').attr("src"));
            $('#logo').attr("src", "/static/img/default-image.jpg");
            $($(this).parent().children('.custom-file-label')[0]).html('Загрузите файл');
        }
    });

    $('#id_banner').change(function(event){
        if(typeof event.target.files[0] !== 'undefined'){
            $('#banner').attr("src", URL.createObjectURL(event.target.files[0]));
            $($(this).parent().children('.custom-file-label')[0]).html(event.target.files[0].name);
        }
        else {
            URL.revokeObjectURL($('#banner').attr("src"));
            $('#banner').attr("src", "/static/img/default-image.jpg");
            $($(this).parent().children('.custom-file-label')[0]).html('Загрузите файл');
        }
    });

    $('.col-md-6', $('#images')).each(function(){
        var uploadButton = $(this).children('.card').children('.card-body').children('.form-group').children('.input-group').children('.custom-file').children('input')[0];
        onImageButtonUpload(uploadButton);
    });

    $('#add_more').click(function() {
        for(var ind=0; ind<4; ind++){
            var form_idx = $('#id_cinema_gallery-TOTAL_FORMS').val();
            $('#images').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
            var totalForms = parseInt(form_idx) + 1;
            $('#id_cinema_gallery-TOTAL_FORMS').val(totalForms);
            
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
            $(image_id).attr("src", "/static/img/default-image.jpg");
            $($(this).parent().children('.custom-file-label')[0]).html('Загрузите файл');
        }
        $('.card.ms-2').matchHeight();
    });
}

function deleteImage(button){
    $(button).parent().parent().remove();  
}


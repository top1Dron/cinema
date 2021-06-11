$('#id_description_ru').summernote({
    height: '200px',
});

$('#id_description_uk').summernote({
    height: '200px',
});

$('#id_seo_description').summernote({
    height: '200px',
});

$('#id_main_image').change(function(event){
    if(typeof event.target.files[0] !== 'undefined'){
        $('#main_image').attr("src", URL.createObjectURL(event.target.files[0]));
    }
    else {
        URL.revokeObjectURL($('#main_image').attr("src"));
        $('#main_image').attr("src", "{% static 'img/default-image.jpg' %}")
    }
});

$('.col-md-6', $('#images')).each(function(){
    // console.log($(this));
    img = $(this).children('.card').children('img')[0];
    uploadButton = $(this).children('.card').children('.card-body').children('input')[0];
    
    upload_id = '#' + uploadButton.getAttribute('id');
    image_id = '#' + img.getAttribute('id');
    $(upload_id).change(function(event){
        image_id = '#' + $(this).parent().parent().children('img')[0].getAttribute('id');
        if(typeof event.target.files[0] !== 'undefined'){
            $(image_id).attr("src", URL.createObjectURL(event.target.files[0]));
        }
        else {
            URL.revokeObjectURL($(image_id).attr("src"));
            $(image_id).attr("src", "{% static 'img/default-image.jpg' %}")
        }
    });
});

function deleteImage(button){
    $(button).parent().parent().remove();  
}

$('#add_more').click(function() {
    for(var ind=0; ind<4; ind++){
        var form_idx = $('#id_stock_gallery-TOTAL_FORMS').val();
        $('#images').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
        var totalForms = parseInt(form_idx) + 1;
        $('#id_stock_gallery-TOTAL_FORMS').val(totalForms);
        
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

$("input[data-bootstrap-switch]").each(function(){
    $(this).bootstrapSwitch('state', $(this).prop('checked'));
});
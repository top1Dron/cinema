$('#id_backgroung_image').change(function(event){
    if(typeof event.target.files[0] !== 'undefined'){
        $('#backgroung_image').attr("src", URL.createObjectURL(event.target.files[0]));
    }
    else {
        URL.revokeObjectURL($('#backgroung_image').attr("src"));
        $('#backgroung_image').attr("src", "{% static 'img/default-image.jpg' %}")
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
$.each(['#news_and_stock_adv_gallery_images', '#main_gallery_images'], function(i, item){
    $('.col-md-6', $(item)).each(function(){
        uploadButton = $(this).children('.card').children('.card-body').children('input')[0];
        onImageButtonUpload(uploadButton);
    });
});

$('#main_gallery_add_more').click(function() {
    for(var ind=0; ind<4; ind++){
        var form_idx = $('#main_gallery_images').parent().children('#id_on_top_main-TOTAL_FORMS').val();
        $('#main_gallery_images').append($('#main_gallery_empty_form').html().replace(/__prefix__/g, form_idx));
        var totalForms = parseInt(form_idx) + 1;
        $('#main_gallery_images').parent().children('#id_on_top_main-TOTAL_FORMS').val(totalForms);
        
        var imageColumn = $('#main_gallery_images').children('.col-md-6').last();
        var img = $(imageColumn).children('.card').children('img')[0];
        var image_id = img.getAttribute('id') + totalForms.toString();
        $(img).attr('id', image_id);
        var uploadButton = $(imageColumn).children('.card').children('.card-body').children('input')[0];
        onImageButtonUpload(uploadButton);
    }
});

function add_images_to_formset(formset_id){
    var form_idx = $('#id_on_top_main-TOTAL_FORMS').val();
    $(`#${formset_id}`).append($(`#${formset_id}_empty_form`).html().replace(/__prefix__/g, form_idx));
    var totalForms = parseInt(form_idx) + 1;
    $('#id_on_top_main-TOTAL_FORMS').val(totalForms);
    
    var imageColumn = $(formset_id).children('.col-md-6').last();
    var img = $(imageColumn).children('.card').children('img')[0];
    var image_id = img.getAttribute('id') + totalForms.toString();
    $(img).attr('id', image_id);
    var uploadButton = $(imageColumn).children('.card').children('.card-body').children('input')[0];
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
                $(`#id_on_top_main-${form_ind}-DELETE`).attr('checked', true);
                $(button).parent().parent().addClass("d-none");
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
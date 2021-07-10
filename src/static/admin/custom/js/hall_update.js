$(document).ready(function(){
    $('#id_description_ru').summernote({
        height: '200px',
    });
    
    $('#id_description_uk').summernote({
        height: '200px',
    });

    $('.card.ms-2').matchHeight();

    $('#id_banner').change(function(event){
        if(typeof event.target.files[0] !== 'undefined'){
            $('#banner').attr("src", URL.createObjectURL(event.target.files[0]));
            $($(this).parent().children('.custom-file-label')[0]).html(event.target.files[0].name);
        }
        else {
            URL.revokeObjectURL($('#banner').attr("src"));
            if($('#banner').attr("image-start-src") == "..."){
                $('#banner').attr("src", "/static/img/default-image.jpg");
            }
            else{
                $('#banner').attr("src", $('#banner').attr("image-start-src"));
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
            var form_idx = $('#id_hall_gallery-TOTAL_FORMS').val();
            $('#images').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
            var totalForms = parseInt(form_idx) + 1;
            $('#id_hall_gallery-TOTAL_FORMS').val(totalForms);
            
            var imageColumn = $('#images').children('.col-md-6').last();
            var img = $(imageColumn).children('.card').children('img')[0];
            var image_id = img.getAttribute('id') + totalForms.toString();
            $(img).attr('id', image_id);
            var uploadButton = $(imageColumn).children('.card').children('.card-body').children('.form-group').children('.input-group').children('.custom-file').children('input')[0];
            onImageButtonUpload(uploadButton);
        }
    });
    
    $('#col_input').on('input', function(e){checkBuildShemeButtonAvailable()});
    $('#row_input').on('input', function(e){checkBuildShemeButtonAvailable()});

    $('#create_scheme_button').click(function(){
        $.fn.reverse = [].reverse;
        var url = $(this).attr('check-available');
        $.getJSON(url, function(data) {
            if(data['any']){
                $('#errorHallSchemeCreationModal').modal();
                $('#row_input').val('');
                $('#col_input').val('');
            }
            else {
                $('#id_hall_scheme').empty();
                var rows = $('#row_input').val();
                var cols = $('#col_input').val();
                if(!$.isNumeric(rows) || $.isNumeric(rows) && rows < 0 || !$.isNumeric(cols) || $.isNumeric(cols) && cols < 0){
                    $('#row_input').val('');
                    $('#col_input').val('');
                    return;
                }
                for(var row_num = 1; row_num <= rows; row_num++){
                    // create row
                    jQuery('<div/>', {
                        id: `row_${row_num}`,
                        "class": 'row justify-content-center mt-2',
                    }).appendTo('#id_hall_scheme');
                    jQuery('<label/>', {
                        for: `row_${row_num}`,
                        "class": 'col-1 d-flex align-items-center form-col-label',
                        html: `Ряд ${row_num}`,
                    }).appendTo(`#row_${row_num}`);
                    for(var col_num=1; col_num <= cols; col_num++){
                        var px = 50;
                        if(cols > 17 && cols < 20){
                            px = 45;
                        }
                        else if(cols > 19 && cols < 22){
                            px = 40;
                        }
                        else if(cols >= 22 && cols < 24){
                            px = 35;
                        }
                        else if(cols >= 24 && cols < 27){
                            px = 30;
                        }
                        else if(cols >= 27){
                            px = 27;
                        }
                        // create col
                        jQuery('<div/>', {
                            id: `row_${row_num}_col_${col_num}`,
                            
                        }).appendTo(`#row_${row_num}`);

                        // create btn inside col
                        jQuery('<button/>', {
                            "data-toggle": "dropdown",
                            "aria-haspopup": "true", 
                            "aria-expanded": "false", 
                            type:"button",
                            "pos": `${col_num}`,
                            "class": 'badge badge-info m-1 text-wrap',
                            style: `height:${px}px; width:${px}px;`,
                            id: `row_${row_num}_col_${col_num}_btn`,
                        }).appendTo(`#row_${row_num}_col_${col_num}`);
                        
                        // create btn value inside span (much easier to get value)
                        jQuery('<span/>', {
                            "class": '',
                            html: `${col_num}`,
                        }).appendTo(`#row_${row_num}_col_${col_num}_btn`);
                        
                        // create dropdown menu which shows on btn click
                        jQuery('<div/>', {
                            id: `row_${row_num}_col_${col_num}_btn_dropdown`,
                            "class": 'dropdown-menu',
                        }).appendTo(`#row_${row_num}_col_${col_num}`);

                        // item remove-append (make place empty)
                        jQuery('<div/>', {
                            "class": 'dropdown-item',
                            html: "Убрать/Добавить",
                        }).appendTo(`#row_${row_num}_col_${col_num}_btn_dropdown`);
                        $('.dropdown-item', $(`#row_${row_num}_col_${col_num}_btn_dropdown`)).each(function(){
                            $(this).click(function(){
                                var current_number = $(this).parent().parent().children('button').children('span').html();
                                var current_position = $(this).parent().parent().children('button').attr('pos');
                                if ($.isNumeric(current_number)){
                                    $(this).parent().parent().parent().children().each(function(index){
                                        if (index >= parseInt(current_position)){
                                            var new_col_num = $(this).children('button').children('span').html();
                                            if ($.isNumeric(new_col_num)){
                                                new_col_num = parseInt(new_col_num) - 1;
                                            }
                                            $(this).children('button').children('span').html(new_col_num);
                                        }
                                    });
                                    var emptyVal = ' ';
                                    //make vip btn unavailable until number not set
                                    var vipBtn = $(this).parent().parent().children('.dropdown-menu').children('.dropdown-item')[1];
                                    $(vipBtn).addClass( "d-none");

                                    $(this).parent().parent().children('button').removeClass('badge-info badge-success');
                                    $(this).parent().parent().children('button').addClass('badge-primary');
                                    $(this).parent().parent().children('button').children('span').html((emptyVal));
                                    $('#json_scheme').val(createJsonScheme());
                                }
                                else{
                                    // iter to find new current number
                                    var rev = false;
                                    var iter_col_num = '';
                                    $(this).parent().parent().parent().children().each(function(index){
                                        if (index >= parseInt(current_position)){
                                            iter_col_num = $(this).children('button').children('span').html();
                                            if($.isNumeric(iter_col_num)){
                                                return false;
                                            }
                                        }
                                    });

                                    if(!$.isNumeric(iter_col_num)){
                                        $(this).parent().parent().parent().children().reverse().each(function(index){
                                            if (index < parseInt(current_position)){
                                                iter_col_num = $(this).children('button').children('span').html();
                                                if($.isNumeric(iter_col_num)){
                                                    rev = true;
                                                    return false;
                                                }
                                            }
                                        });
                                    }

                                    //iter to set new values to next places in the row
                                    $(this).parent().parent().parent().children().each(function(index){
                                        if (index >= parseInt(current_position)){
                                            var new_col_num = $(this).children('button').children('span').html();
                                            if($.isNumeric(new_col_num)){
                                                new_col_num = parseInt(new_col_num) + 1;
                                            }
                                            $(this).children('button').children('span').html(new_col_num);
                                        }
                                    });
                                    //make vip btn available
                                    var vipBtn = $(this).parent().parent().children('.dropdown-menu').children('.dropdown-item')[1];
                                    $(vipBtn).removeClass( "d-none");
                                    if(!$.isNumeric(iter_col_num)){
                                        iter_col_num = 1;
                                    }
                                    else if(rev){
                                        iter_col_num++;
                                        rev = false;
                                    }
                                    $(this).parent().parent().children('button').children('span').html(iter_col_num);
                                    $(this).parent().parent().children('button').removeClass('badge-primary');
                                    $(this).parent().parent().children('button').addClass('badge-info');
                                    $('#json_scheme').val(createJsonScheme());
                                }
                            });
                        });

                        // item make VIP place 
                        jQuery('<div/>', {
                            "class": 'dropdown-item',
                            html: "Сделать VIP",
                        }).appendTo(`#row_${row_num}_col_${col_num}_btn_dropdown`).click(function(){
                            if($(this).parent().parent().children('button').hasClass('badge-success')){
                                $(this).parent().parent().children('button').removeClass('badge-success');
                                $(this).parent().parent().children('button').addClass('badge-info');
                            }
                            else {
                                $(this).parent().parent().children('button').removeClass('badge-info');
                                $(this).parent().parent().children('button').addClass('badge-success');
                            }
                            $('#json_scheme').val(createJsonScheme());
                        });
                        $('#json_scheme').val(createJsonScheme());
                    }
                }
                
            }
            $('#row_input').val('');
            $('#col_input').val('');
        });
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
                $(`#id_hall_gallery-${form_ind}-DELETE`).attr('checked', true);
                $(button).parent().parent().addClass("d-none");
            }
        });
    }
    else{
        $(button).parent().parent().remove();
    }
    $('#id_hall_gallery-TOTAL_FORMS').val($('#id_hall_gallery-TOTAL_FORMS').val() - 1);
    $('.card.ms-2').matchHeight(); 
}

function getCookie(name) {

    var matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ))
    return matches ? decodeURIComponent(matches[1]) : undefined
};

function createJsonScheme(){
    var json_scheme = {};
    var row = 0;
    $('#id_hall_scheme').children().each(function(i){
        var row_place;
        if (check_row_available(`#row_${i+1}`)){
            row++;
            row_place = row;
            $(`label[for=row_${i+1}]`).html(`Ряд ${row_place}`);
        }
        else {
            row_place = ' ';
            $(`label[for=row_${i+1}]`).html('\t');
        }
        $(this).children(':not(label)').each(function(j){
            var isVip = $(this).children('button').hasClass('badge-success');
            let place = {
                real_row: i + 1,
                row: row_place,
                real_pos: $(this).children('button').attr('pos'),
                number: $(this).children('button').children('span').html(),
                vip: isVip
            };
            json_scheme[`${place.real_row}_${place.real_pos}`] = place;
        });
    });
    return JSON.stringify(json_scheme);
}

function check_row_available(row){
    var available = false;
    $(row).children().each(function(i){
        $(this).children('button').each(function(j){
            if($(this).hasClass('badge-info') || $(this).hasClass('badge-success')){
                available = true;
                return false;
            }
        });
    });
    return available;
}

function checkBuildShemeButtonAvailable(){
    if($('#row_input').val() && $('#col_input').val()){
        $('#create_scheme_button').prop( "disabled", false );
    }
    else{
        $('#create_scheme_button').prop( "disabled", true );
    }
   
}
$(document).ready(function(){
    $("#startdatetime").datetimepicker({
        format: "DD.MM.YYYY HH:mm",
        weekStart: 1,
        todayBtn:  1,
        autoclose: 1,
        todayHighlight: 1,
        startView: 2,
        minView: 2,
        minDate: $.now(),
    });



    $('.dropdown-item').on('click', function(event){
        event.preventDefault();
        var button = $(this).parent().parent().children('button');
        var isVIP = $(button).attr('vip');
        var menu = $(this).parent();
        var update_url = $(button).attr('ticket-update-url');
        if($(this).hasClass('book')){
            $(menu).children().removeClass('d-none');
            $(this).removeClass('book');
            $(this).addClass('free');
            $(this).children('span').html('Освободить');
            if(isVIP == 'True'){
                $(button).addClass('bg-gradient-warning');
            }
            else {
                $(button).addClass('bg-gradient-primary');
            }
            updateTicket(update_url, '1');
            
            // var bookedMoney = $('booked_money').html();
        }
        else if($(this).hasClass('free')){
            $(menu).children().removeClass('d-none');
            $(this).removeClass('free');
            $(this).addClass('book');
            $(this).children('span').html('Забронировать');
            if(isVIP == 'True'){
                $(button).removeClass('bg-gradient-warning');
                $(button).removeClass('bg-gradient-danger');
            }
            else {
                $(button).removeClass('bg-gradient-primary');
                $(button).removeClass('bg-gradient-dark');
            }
            updateTicket(update_url, '0');
        }
        else if($(this).hasClass('sell')){
            if(isVIP == 'True'){
                $(button).addClass('bg-gradient-danger');
                if($(button).hasClass('bg-gradient-warning')){
                    $(button).removeClass('bg-gradient-warning');
                }
            }
            else {
                $(button).addClass('bg-gradient-dark');
                if($(button).hasClass('bg-gradient-primary')){
                    $(button).removeClass('bg-gradient-primary');
                }
            }
            $(this).addClass('d-none');
            $($(menu).children()[0]).removeClass('book');
            $($(menu).children()[0]).removeClass('sell');
            $($(menu).children()[0]).addClass('free');
            $($(menu).children()[0]).children('span').html('Освободить');
            updateTicket(update_url, '2');
        }
    });
})

function getCookie(name) {

    var matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ))
    return matches ? decodeURIComponent(matches[1]) : undefined
};

function updateTicket(update_url, status){
    $.ajax({
        url: update_url,
        type: 'POST',
        data: {
            'status': status,
        },
        dataType: 'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        },
        success: function(resp){
            var responce = resp;
            $('#total_places').html(responce.total_places);
            $('#total_free_places').html(responce.total_free_places);
            $('#total_booked_places').html(responce.total_booked_places);
            $('#booked_money').html(responce.booked_money);
            $('#total_sold_places').html(responce.total_sold_places);
            $('#sold_money').html(responce.sold_money);
        }
    });
}
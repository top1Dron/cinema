$(document).ready(function(){
    var selected_tickets = new Set();
    $('.free').on('click', function(event){
        if($(this).hasClass('bg-info')){
            $(this).removeClass('bg-info');
            $(this).addClass('bg-primary bg-gradient');
            $('#tickets').html(parseInt($('#tickets').html()) + 1);
            $('#summ').html(parseInt($('#summ').html()) + parseInt($('#session_price').attr('price')));
            selected_tickets.add(parseInt($(this).attr('ticket-id')));
        }
        else if($(this).hasClass('bg-success')){
            $(this).removeClass('bg-success');
            $(this).addClass('bg-warning bg-gradient');
            $('#tickets').html(parseInt($('#tickets').html()) + 1);
            $('#summ').html(parseInt($('#summ').html()) + parseInt($('#vip_price').attr('price')));
            selected_tickets.add(parseInt($(this).attr('ticket-id')));
        }
        else if($(this).hasClass('bg-primary bg-gradient')){
            $(this).removeClass('bg-primary bg-gradient');
            $(this).addClass('bg-info');
            $('#tickets').html(parseInt($('#tickets').html()) - 1);
            $('#summ').html(parseInt($('#summ').html()) - parseInt($('#session_price').attr('price')));
            selected_tickets.delete(parseInt($(this).attr('ticket-id')));
        }
        else if($(this).hasClass('bg-warning bg-gradient')){
            $(this).removeClass('bg-warning bg-gradient');
            $(this).addClass('bg-success');
            $('#tickets').html(parseInt($('#tickets').html()) - 1);
            $('#summ').html(parseInt($('#summ').html()) - parseInt($('#vip_price').attr('price')));
            selected_tickets.delete(parseInt($(this).attr('ticket-id')));
        }
        $('#id_selected_tickets1').val(Array.from(selected_tickets).join(' '));
        $('#id_selected_tickets2').val(Array.from(selected_tickets).join(' '));
    });
})
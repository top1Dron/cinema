$(document).ready(function(){
    $('#afiche_btn').click(function(){
        $(this).removeClass('btn-light');
        $(this).addClass('btn-success');
        $('#soon_btn').removeClass('btn-success');
        $('#soon_btn').addClass('btn-light');
        $('#id_active_movies').addClass('d-block');
        $('#id_active_movies').removeClass('d-none');
        $('#id_soon_movies').addClass('d-none');
        $('#id_active_movies').removeClass('d-block');
    });
    $('#soon_btn').click(function(){
        $(this).removeClass('btn-light');
        $(this).addClass('btn-success');
        $('#afiche_btn').removeClass('btn-success');
        $('#afiche_btn').addClass('btn-light');
        $('#id_soon_movies').addClass('d-block');
        $('#id_soon_movies').removeClass('d-none');
        $('#id_active_movies').addClass('d-none');
        $('#id_active_movies').removeClass('d-block');
    });
})
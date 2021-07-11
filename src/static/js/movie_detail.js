$(document).ready(function(){
    var shedule_shown = false;
    $('#movie_info_btn').click(function(){
        $(this).removeClass('btn-outline-success');
        $(this).addClass('btn-success');
        $('#movie_shedule_btn').removeClass('btn-success');
        $('#movie_shedule_btn').addClass('btn-outline-success');
        $('#movie_info').removeClass('d-none');
        $('#movie_info').addClass('d-block');
        $('#movie_shedule').removeClass('d-block');
        $('#movie_shedule').addClass('d-none');
    });
    $('#movie_shedule_btn').click(function(){
        $(this).removeClass('btn-outline-success');
        $(this).addClass('btn-success');
        $('#movie_info_btn').removeClass('btn-success');
        $('#movie_info_btn').addClass('btn-outline-success');
        $('#movie_shedule').removeClass('d-none');
        $('#movie_shedule').addClass('d-block');
        $('#movie_info').removeClass('d-block');
        $('#movie_info').addClass('d-none');
        if (!shedule_shown){
            $('#id_shedule_table').DataTable({
                "paging": false,
                "lengthChange": false,
                "searching": false,
                "ordering": false,
                "info": false,
                "autoWidth": false,
                "responsive": true,
            });
            shedule_shown = true;
        }
    });
})
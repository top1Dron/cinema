$(document).ready(function(){
    $('#id_email').change(function(event){
        $('#current_template').html(event.target.files[0].name);
        $('#id_file_id').attr('value', 'new');
    });
    $('input[type=radio][name=recipients]').change(function() {
        if (this.value == '0') {
            $('#chooseUsers').prop( "disabled", true );
        }
        else if (this.value == '1') {
            $('#chooseUsers').prop( "disabled", false );
        }
    });
    $('#users_table').DataTable({
        "responsive": true, 
        "lengthChange": false, 
        "autoWidth": true,
    }).buttons().container().appendTo('#users_table_wrapper .col-md-6:eq(0)');
    $('input[type=radio][name=mails]').change(function() {
        var label = $(this).parent().children('.form-check-label')[0];
        $('#current_template').html($.trim($(label).text()));
        $('#id_file_id').attr('value', $(this).attr('id'));
    });
    $('#select_users').click(function(){
        var users = [];
        $('.form-check-input:checkbox:checked').each(function(){
            var sThisVal = (this.checked ? $(this).val() : "");
            users.push(sThisVal);
        });
        $('#users').val(users);
    });
    $('.delete-email').each(function(){
        $(this).click(function(){
            var delete_url = $(this).attr('delete-url');
            if (delete_url != null){
                $.ajax({
                    url: delete_url,
                    type: 'DELETE',
                    data: {},
                    beforeSend: function (xhr) {
                        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
                    },
                    success: function(resp){
                        location.href = location.href;
                    }
                });
            }
        })
    })
})

function getCookie(name) {

    var matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ))
    return matches ? decodeURIComponent(matches[1]) : undefined
};
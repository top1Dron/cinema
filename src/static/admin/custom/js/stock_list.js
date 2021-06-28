function deleteStock(button){
    if(confirm('Вы уверены, что хотите удалить данные об этой акции из базы данных?')){
        deleteUrl = $(button).attr("delete-url");
        $.ajax({
            url: deleteUrl,
            type: 'DELETE',
            data: {},
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
            success: function(resp){
                alert("Данные об этой акции успешно удалены");
                window.location.reload();
            }
        });
    }
}

function getCookie(name) {

    var matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ))
    return matches ? decodeURIComponent(matches[1]) : undefined
};

$(function () {
    $('#stock_table').DataTable({
      "paging": true,
      "lengthChange": false,
      "searching": false,
      "ordering": true,
      "info": true,
      "autoWidth": false,
      "responsive": true,
      "columnDefs": [
        {
          "targets": [3], 
          "orderable": false, 
          "visible": true }
      ]
    });
});
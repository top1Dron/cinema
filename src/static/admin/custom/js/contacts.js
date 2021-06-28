$(document).ready(function(){
    // $('.cinema-logo-btn').each(function(){
    //     $(this).change(function(event){
    //         image_id = '#' + $(this).parent().children('img')[0].getAttribute('id');
    //         console.log(image_id);
    //         if(typeof event.target.files[0] !== 'undefined'){
    //             $(image_id).attr("src", URL.createObjectURL(event.target.files[0]));
    //         }
    //         else {
    //             URL.revokeObjectURL($(image_id).attr("src"));
    //             $(image_id).attr("src", "/static/img/default-image.jpg")
    //         }
    //     });
    // })
})

function onImageUpload(uploadButton){
    console.log(uploadButton);
    image_id = '#' + $(uploadButton).parent().children('img')[0].getAttribute('id');
    console.log(image_id);
    if(typeof event.target.files[0] !== 'undefined'){
        $(image_id).attr("src", URL.createObjectURL(event.target.files[0]));
    }
    else {
        URL.revokeObjectURL($(image_id).attr("src"));
        $(image_id).attr("src", "/static/img/default-image.jpg")
    }
}
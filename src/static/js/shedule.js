$(document).ready(function(){
    $('#id_movie').on('change', function(e){
        var search = window.location.search;
        search = replaceQueryParam('hall', false, search);
        document.location.href = updateURLParameter(
            search, 
            'movie', 
            $('#id_movie').val());
    });
    $('#id_cinema').on('change', function(e){
        var search = window.location.search;
        search = replaceQueryParam('hall', false, search);
        document.location.href = updateURLParameter(
            search, 
            'cinema', 
            $('#id_cinema').val());
    });
    $('#id_format').on('change', function(e){
        var search = window.location.search;
        search = replaceQueryParam('hall', false, search);
        document.location.href = updateURLParameter(
            search, 
            'format', 
            $('#id_format').val());
    });

    $('#id_today_sessions_radio').click(function(){
        $('.sessions').removeClass('d-block');
        $('.sessions').addClass('d-none');
        $('#id_today_sessions').removeClass('d-none');
        $('#id_today_sessions').addClass('d-block');
    });
    $('#id_all_session_radio').click(function(){
        $('.sessions').removeClass('d-block');
        $('.sessions').addClass('d-none');
        $('#id_all_sessions').removeClass('d-none');
        $('#id_all_sessions').addClass('d-block');
    });
    $('#id_tomorrow_session_radio').click(function(){
        $('.sessions').removeClass('d-block');
        $('.sessions').addClass('d-none');
        $('#id_tomorrow_sessions').removeClass('d-none');
        $('#id_tomorrow_sessions').addClass('d-block');
    });
    $('#id_week_session_radio').click(function(){
        $('.sessions').removeClass('d-block');
        $('.sessions').addClass('d-none');
        $('#id_next_week_sessions').removeClass('d-none');
        $('#id_next_week_sessions').addClass('d-block');
    });
})

function updateURLParameter(url, param, paramVal)
{
    var TheAnchor = null;
    var newAdditionalURL = "";
    var tempArray = url.split("?");
    var baseURL = tempArray[0];
    var additionalURL = tempArray[1];
    var temp = "";

    if (additionalURL) 
    {
        var tmpAnchor = additionalURL.split("#");
        var TheParams = tmpAnchor[0];
            TheAnchor = tmpAnchor[1];
        if(TheAnchor)
            additionalURL = TheParams;

        tempArray = additionalURL.split("&");

        for (var i=0; i<tempArray.length; i++)
        {
            if(tempArray[i].split('=')[0] != param)
            {
                newAdditionalURL += temp + tempArray[i];
                temp = "&";
            }
        }        
    }
    else
    {
        var tmpAnchor = baseURL.split("#");
        var TheParams = tmpAnchor[0];
            TheAnchor  = tmpAnchor[1];

        if(TheParams)
            baseURL = TheParams;
    }

    if(TheAnchor)
        paramVal += "#" + TheAnchor;

    var rows_txt = "";
    if (paramVal){
        rows_txt += temp + "" + param + "=" + paramVal;
    }
    
    return baseURL + "?" + newAdditionalURL + rows_txt;
}

function replaceQueryParam(param, newval, search) {
    var regex = new RegExp("([?;&])" + param + "[^&;]*[;&]?");
    var query = search.replace(regex, "$1").replace(/&$/, '');

    return (query.length > 2 ? query + "&" : "?") + (newval ? param + "=" + newval : '');
}
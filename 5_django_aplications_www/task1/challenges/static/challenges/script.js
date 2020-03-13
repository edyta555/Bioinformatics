$(document).ready(function() {
    $('.plus-button').click(function() {
        var tr = $(this).parent().parent(); 
        var pk = tr.prop('id');
        $.get('/ajax/increment?id=' + pk, function(data) {
	    /* zmiana w wierszu */
	    tr.find('.counter').text(data.counter);
            tr.find('.fraction-text').text(data.fraction);
        });
    });

    function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
    };

    $('.ajax-save').click(
    function() {
        var tr = $(this).parent().parent();
        var csrftoken = getCookie('csrftoken');
        var pk = tr.prop('id');
        var ver = tr.prop('version');
        
        var name = tr.find('.name-edit').val();
        var days = tr.find('.days-edit').val();
        var description = tr.find('.description-edit').val();
        var begin = tr.find('.begin-edit').val();
        var counter = tr.find('.counter-edit').val();
        $.post('/ajax/save/',
		{ 'csrfmiddlewaretoken': csrftoken,
		  'id': pk,
		  'name': name,
		  'days': days,
                  'ver':  ver,
		  'begin': begin,
		  'description': description,
		  'counter': counter
		},
	function(data) {
            if (data == '0') {
                tr.find('.name-text').text(name);
                tr.find('.days-text').text(days);
                tr.find('.description-text').text(description);
                tr.find('.counter-text').text(counter);
            } 
        });

        $.get('/ajax/getData?id=' + pk, function(data) {
	    /* zmiana w wierszu */
            tr.find('.fraction-text').text(data.fraction);
            tr.find('.begin-text').text(data.begin);
         });
    });

    $(".ajax-delete").click(
    function(){
        var tr = $(this).parent().parent();
        var csrftoken = getCookie('csrftoken');
        var pk = tr.prop('id');
      $.post('/ajax/delete/',
		{ 'csrfmiddlewaretoken': csrftoken,
		  'id': pk}
            );
    });

    $('.ajax-edit').click(function() {
	var tr = $(this).parent().parent();
	var csrftoken = getCookie('csrftoken');
	var pk = tr.prop('id');
	
	$.post('/ajax/getChallenge/', { 'csrfmiddlewaretoken': csrftoken, 'id': pk }, function(data) {
		var dataDict = JSON.parse(data);
                tr.find('.name-edit').val(dataDict["name"]);
                tr.find('.days-edit').val(dataDict["days"]);
                tr.find('.description-edit').val(dataDict["description"]);
                tr.find('.counter-edit').val(dataDict["counter"]);
                tr.find('.begin-edit').val(dataDict["begin"]);
                tr.prop('version', dataDict["ver"]);
	});
    });


        $('.return-button').hide();
        $('.edit').hide();
  	$('.edit-button').click(function(){
	    var tr = $(this).parent().parent();
	    tr.find('.edit-button').hide();
	    tr.find('.delete-button').hide();
            tr.find('.plus-button').hide();
	    tr.find('.return-button').show();
	    tr.find('.edit').show();
            tr.find('.text').hide();
        });
  	$('.delete-button').click(function(){
	    $(this).parent().parent().hide();
	});
        $('.return-button').click(function(){
    	    var tr = $(this).parent().parent();
	    tr.find('.text').show();
	    tr.find('.edit-button').show();
	    tr.find('.delete-button').show();
            tr.find('.plus-button').show();
	    tr.find('.edit').hide();
            tr.find('.return-button').hide();
        });
});


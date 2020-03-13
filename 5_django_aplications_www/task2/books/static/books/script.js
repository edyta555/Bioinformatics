$(document).ready(function() {
    $('.comments_edit').hide();
    $('.save-button').hide();
    $('.cancel-button').hide();


    $('.edit-button').click(function() {
        var tr = $(this).parent().parent();
        tr.find('.comments').hide();
        tr.find('.comments_edit').show();
        tr.find('.edit-button').hide();
        tr.find('.delete-button').hide();
        tr.find('.save-button').show();
        tr.find('.cancel-button').show();
        var csrftoken = getCookie('csrftoken');
        var pk = tr.prop('id');
        $.post('/ajax/getBook/', { 'csrfmiddlewaretoken': csrftoken, 'id': pk }, function(data) {
          var dataDict = JSON.parse(data);
          tr.find('.comments_edit').val(dataDict['comments']);
          tr.attr('version', dataDict['version']);
        });
    });
    
     $('.check-button').click(function() {
      var tr = $(this).parent().parent();
      var csrftoken = getCookie('csrftoken');
      var pk = tr.prop('id');
      var version = tr.attr('version');
      //alert(version);
      $.post('/ajax/changeWasRead/',
      { 'csrfmiddlewaretoken': csrftoken, 'id': pk, 'version': version}, function(data) {//data kod bledu
      var dataDict = JSON.parse(data);
      tr.attr('version', dataDict['version']);
      if ( dataDict['ret'] == 1){
          alert("Change did not succeed. Try again.");
      }
      if (dataDict['wasRead'] == 1){
        $(this).prop('checked', true);
      } else {
        $(this).prop('checked', false);  
      }
      
      
        });
    });

    $('.save-button').click(function() {
      var tr = $(this).parent().parent();
          tr.find('.comments').show();
          tr.find('.edit-button').show();
      tr.find('.delete-button').show();
          tr.find('.comments_edit').hide();
          tr.find('.save-button').hide();
      tr.find('.cancel-button').hide();
      //Ajax
      var csrftoken = getCookie('csrftoken');
      var pk = tr.prop('id');
      var comments = tr.find('.comments_edit').val();
      var version = tr.attr('version');
      $.post('/ajax/save/',
      { 'csrfmiddlewaretoken': csrftoken,
      'id': pk,
      'comments': comments,
      'version': version
      },
      function(data) {
          if (data == '0') {
            tr.find('.comments').each(function() {
                  $(this).text($(this).next().val());
              });
          }
          else{
            alert("Change did not succeed. Try again.");
            $.post('/ajax/getBook/', { 'csrfmiddlewaretoken': csrftoken, 'id': pk }, function(data) {
              var dataDict = JSON.parse(data);
              tr.find('.comments').text(dataDict['comments']);
              tr.find('.category').text(dataDict['category']);
 
            });
          }
      });
    });

    $('.cancel-button').click(function() {
      var tr = $(this).parent().parent();
      tr.find('.comments').show();
      tr.find('.edit-button').show();
      tr.find('.delete-button').show();
      tr.find('.save-button').hide();
      tr.find('.cancel-button').hide();
      var csrftoken = getCookie('csrftoken');
      var pk = tr.prop('id');
      $.post('/ajax/getBook/', { 'csrfmiddlewaretoken': csrftoken, 'id': pk }, function(data) {
        var dataDict = JSON.parse(data);
        tr.find('.comments').text(dataDict['comments']);
      });
      tr.find('.comments_edit').hide();

    });

    $('.delete-button').click(function(){
      var tr = $(this).parent().parent();
      var csrftoken = getCookie('csrftoken');

      pk=tr.prop('id');
      $.post('/ajax/delete/',
      { 'csrfmiddlewaretoken': csrftoken,
        'id': pk,
      },
      function(data) {
          if (data == '0') {
            tr.hide();
          }
      });
      });
});


// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
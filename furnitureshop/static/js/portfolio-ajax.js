$('#likes').click(function(){
  var catid;
  catid = $(this).attr("data-catid");
  $.get('/portfolio/like/', {category_id: catid}, function(data){
      $('#like_count').html(data);
          $('#likes').hide();
        });
});

$('#suggestion').keyup(function(){
  var query;
  query = $(this).val();
  $.get('/portfolio/suggest/', {suggestion: query}, function(data){
        $('#cats').html(data);
        });
});

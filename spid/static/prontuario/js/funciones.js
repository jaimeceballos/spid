$(document).ready(function(){

  $("#nuevo").click(function(event){
      event.preventDefault();
      var url = '/prontuario/nuevo/';
      $.get(url,function(data){
        $("#contenido").hide().empty().append(data).slideDown(1000);
      })
  });

});

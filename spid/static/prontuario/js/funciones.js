$(document).ready(function(){
  $("#verificar").click(function(event){
    event.preventDefault();
    var url = "/prontuario/verificar/";
    $.get(url,function(data){
      $("#contenido").empty().append(data);
    });
  });
  $("#nuevo").click(function(event){
      event.preventDefault();
      var url = '/prontuario/nuevo/';
      $.get(url,function(data){
        $("#contenido").hide().empty().append(data).slideDown(1000);
      })
  });
  $("#buscar").click(function(event){
      event.preventDefault();
      var url = '/prontuario/buscar/';
      $.get(url,function(data){
        $("#contenido").hide().empty().append(data).slideDown(1000);
      })
  });
});

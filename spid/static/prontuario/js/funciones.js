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
      $("#contenido").hide().empty().append('<h3> Cargando <img src="/static/imagenes/preventivos/loading.gif" id="loading" /> <h3>').show();
      var url = '/prontuario/nuevo/';
      $.get(url,function(data){
          $("#contenido").hide().empty().append(data).slideDown(1000);
      })
  });
  $("#buscar").click(function(event){
      event.preventDefault();
      $("#contenido").hide().empty().append('<h3> Cargando <img src="/static/imagenes/preventivos/loading.gif" id="loading" /> <h3>').show();
      var url = '/prontuario/buscar/';
      $.get(url,function(data){
        $("#contenido").hide().empty().append(data).slideDown(1000);
      })
  });

});
function eliminarHistorial(){
  var url = "/prontuario/eliminar_historial/";
  $("#dialog").html('<img src="/static/imagenes/preventivos/loading.gif" id="loading" />');
  $("#dialog").dialog(
  {
    width: 'auto',
    height: 'auto',
    modal:true,
    open: function(event, ui)
    {

    }
  });
  $.get(url,function(data){

  })
  .done(function(data){
    $("#dialog").html(data);
  })
  .fail(function(data){
    $("#dialog").html(data);
  });
}

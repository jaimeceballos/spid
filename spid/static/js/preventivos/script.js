/*
$(function () {

if (navigator.geolocation)
{
  navigator.geolocation.getCurrentPosition(datos,error);

}
else
{
          alert('Tu navegador no soporta geolocalización.');
  /* var contenedor = document.getElementById("mapa");
    var lat = -43.247954;
    var lng = -65.307255;       
    initialize(lat,lng);
   
}

 function datos(position)
 {
    alert('hola')
    var lat = $('#lat').val();
    var lng = $('#longi').val();
    var latitud = $('#latitud').val();
    var longitud= $('#longitud').val();
    if(latitud != '' && latitud !='None' && longitud != '' && latitud !='None'){
      initializer(latitud,longitud);
    }else{  
      initializer(lat,lng);
    }
  
 }
 function error(err) {
            
            if (err.code == 0) {
              alert("Algo ha salido mal");
            }
            if (err.code == 1) {
              alert("No has aceptado compartir tu posición");
            }
            if (err.code == 2) {
              alert("No se puede obtener la posición actual");
            }
            if (err.code == 3) {
              alert("Hemos superado el tiempo de espera");
            }else{
               initializer(lat,lng);
            }
        }
Controlamos los posibles errores */

 function initializer(lat,lng)
 {
   
     var latlng = new google.maps.LatLng(lat,lng);
     var image="/static/imagenes/preventivos/delitoscontrahonor.png";
     var propiedades =
         {
          center: latlng,
          draggable: true,
          KeyBoardShortcuts: true,
          mapTypeControl: true,
          mapTypeId: google.maps.MapTypeId.HYBRID,
          streetViewControl: true,
          zoom: 15,
         };

         var mapa = new google.maps.Map(document.getElementById('mapa'),propiedades);

  
     var marker = new google.maps.Marker({
     position: latlng, 
     map: mapa,
     draggable: true,
  
     title:"Arrastra el marcador si quieres moverlo para ubicar la calle o lugar del Hecho"
     });
 
 google.maps.event.addListener(marker, 'dragend', function() {
 coordenadas(marker,latlng);
  });
 google.maps.event.addDomListener(window, 'load', initialize);
 geocoder = new google.maps.Geocoder();
  geocoder.geocode({'latLng': marker.getPosition()}, function(results, status)  {
      if (status == google.maps.GeocoderStatus.OK) {
        if (results[0]) {
          $('#callen').val(results[0].formatted_address);
          $('#latitud').val(marker.getPosition().lat());
          $('#longitud').val(marker.getPosition().lng());
        }
      }
    });      
}
  function coordenadas(marker)
  {
    
     geocoder = new google.maps.Geocoder();
     geocoder.geocode({'latLng': marker.getPosition()}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        if (results[0]) {
          $('#callen').val(results[0].formatted_address);
          $('#latitud').val(marker.getPosition().lat());
          $('#longitud').val(marker.getPosition().lng());
        }
      }
    });      
  }
  


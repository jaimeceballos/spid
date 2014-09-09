function initialize(address) {
 
      var geoCoder = new google.maps.Geocoder(address)
      var request = {address:address};
      geoCoder.geocode(request, function(result, status){

      var latlng = new google.maps.LatLng(result[0].geometry.location.lat(), result[0].geometry.location.lng()); 

      var myOptions = {
        zoom: 15,
        center: latlng,
        draggable: true,
        KeyBoardShortcuts: true,
        mapTypeControl: true,
        streetViewControl: true,
        mapTypeId: google.maps.MapTypeId.HYBRID
      };
     var mapa= new google.maps.Map(document.getElementById("mapa"),myOptions);
     var marker = new google.maps.Marker({
     position: latlng, 
     map: mapa,
     draggable: true,
     title:"Arrastra el marcador si quieres moverlo"
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
    });      
}
  function initializes(address) {
  
      var geoCoder = new google.maps.Geocoder(address)
      var request = {address:address};
      geoCoder.geocode(request, function(result, status){
      
      var latlng = new google.maps.LatLng(result[0].geometry.location.lat(), result[0].geometry.location.lng()); 

      var myOptions = {
        zoom: 15,
        center: latlng,
        draggable: true,
        KeyBoardShortcuts: true,
        mapTypeControl: true,
        streetViewControl: true,
        mapTypeId: google.maps.MapTypeId.HYBRID
      };
     var mapa= new google.maps.Map(document.getElementById("mapa"),myOptions);
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
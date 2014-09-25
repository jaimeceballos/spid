

function initiali(latv,lngv,ciudadv,listas)
 {

 var lati='';
 var lngt='';
 var preve='';
 var den='';
 var delis='';
 var idpreve='';
var map;
var TILE_SIZE = 256;
var latlng = new google.maps.LatLng(latv,lngv);

function bound(value, opt_min, opt_max) {
  if (opt_min != null) value = Math.max(value, opt_min);
  if (opt_max != null) value = Math.min(value, opt_max);
  return value;
}

function degreesToRadians(deg) {
  return deg * (Math.PI / 180);
}

function radiansToDegrees(rad) {
  return rad / (Math.PI / 180);
}

/** @constructor */
function MercatorProjection() {
  this.pixelOrigin_ = new google.maps.Point(TILE_SIZE / 2,
      TILE_SIZE / 2);
  this.pixelsPerLonDegree_ = TILE_SIZE / 360;
  this.pixelsPerLonRadian_ = TILE_SIZE / (2 * Math.PI);
}

MercatorProjection.prototype.fromLatLngToPoint = function(latLng,
    opt_point) {
  var me = this;
  var point = opt_point || new google.maps.Point(0, 0);
  var origin = me.pixelOrigin_;

  point.x = origin.x + latLng.lng() * me.pixelsPerLonDegree_;

  // Truncating to 0.9999 effectively limits latitude to 89.189. This is
  // about a third of a tile past the edge of the world tile.
  var siny = bound(Math.sin(degreesToRadians(latLng.lat())), -0.9999,
      0.9999);
  point.y = origin.y + 0.5 * Math.log((1 + siny) / (1 - siny)) *
      -me.pixelsPerLonRadian_;
  return point;
};

MercatorProjection.prototype.fromPointToLatLng = function(point) {
  var me = this;
  var origin = me.pixelOrigin_;
  var lng = (point.x - origin.x) / me.pixelsPerLonDegree_;
  var latRadians = (point.y - origin.y) / -me.pixelsPerLonRadian_;
  var lat = radiansToDegrees(2 * Math.atan(Math.exp(latRadians)) -
      Math.PI / 2);
  return new google.maps.LatLng(lat, lng);
};

function createInfoWindowContent() {
  var numTiles = 1 << map.getZoom();
  var projection = new MercatorProjection();
  var worldCoordinate = projection.fromLatLngToPoint(latlng);
  var pixelCoordinate = new google.maps.Point(
      worldCoordinate.x * numTiles,
      worldCoordinate.y * numTiles);
  var tileCoordinate = new google.maps.Point(
      Math.floor(pixelCoordinate.x / TILE_SIZE),
      Math.floor(pixelCoordinate.y / TILE_SIZE));

  return [
      '<strong style="color:red;font-size:10px;font-family:Arial">'+ciudadv + ' -- CHUBUT -- ARGENTINA'
  ].join('</strong><br>');
}

function initializen(){
  var mapOptions = {
    zoom: 13,
    center: latlng
  };

  map = new google.maps.Map(document.getElementById('mapa'),
      mapOptions);
  /*
  var flightPlanCoordinates = [
    new google.maps.LatLng(-43.25583,-65.323598),
    new google.maps.LatLng(-43.267519,-65.317075),
    new google.maps.LatLng(-43.256768,-65.301883),
    new google.maps.LatLng(-43.260956,-65.295188),
    new google.maps.LatLng(-43.247141,-65.27622),
    new google.maps.LatLng(-43.245703,-65.278237),
    new google.maps.LatLng(-43.249329,-65.303214),
    new google.maps.LatLng(-43.255643,-65.323641)
  ];
  var flightPath = new google.maps.Polyline({
    path: flightPlanCoordinates,
    geodesic: true,
    strokeColor: '#FF0000',
    strokeOpacity: 1.0,
    strokeWeight: 2
  });

  flightPath.setMap(map); */


  var image="/static/imagenes/preventivos/";
  var coordInfoWindow = new google.maps.InfoWindow();
  coordInfoWindow.setContent(createInfoWindowContent());
  coordInfoWindow.setPosition(latlng);
  coordInfoWindow.open(map);

  google.maps.event.addListener(map, 'zoom_changed', function() {
    coordInfoWindow.setContent(createInfoWindowContent());
    coordInfoWindow.open(map);
  });

 var infoWindow = new google.maps.InfoWindow;
 var vecesl=listas.split("latitud").length-1
 var vecesln=listas.split("longitud").length-1

for (j=0;j<vecesl;j++){
        var id = listas.indexOf("id"+String(j))+7;
        var lat1 = listas.indexOf("latitud"+String(j))+12; 
        var lng1 = listas.indexOf("longitud"+String(j))+13; 
        var prev=listas.indexOf("prev"+String(j))+9; 
        var denun=listas.indexOf("denuncia"+String(j))+13; 
        var delitos=listas.indexOf("delitos"+String(j))+12; 
      
        if (listas.charAt(id)=="'"){
         
           var tamaid=("id"+String(j)).length
           
           var id = listas.indexOf("id"+String(j))+tamaid+4; 
           
         }
         
         for (i=id;i<listas.length;i++){
         
           if (listas[i]=="'"){
              i=listas.length+2;
              
           }else{
        
           
             idpreve=idpreve+String(listas[i]);

           }
          
          
         }
        
       
        if (listas.charAt(delitos)=="'"){
          var tamadel=("delitos"+String(j)).length
          var delitos = listas.indexOf("delitos"+String(j))+tamadel+4; 
        }
    
         for (i=delitos;i<listas.length;i++){
           if (listas[i]=="'"){
              i=listas.length+2;
      
           }else{
             delis=delis+String(listas[i]);
          }
        
          
         }

        

         if (listas.charAt(prev)=="'"){
          var tamapr=("prev"+String(j)).length
          var prev = listas.indexOf("prev"+String(j))+tamapr+4; 
         }
         for (i=prev;i<listas.length;i++){
           if (listas[i]=="'"){
              i=listas.length+2;
      
           }else{
             
             preve=preve+String(listas[i]);
          }
        
          
         }
      
        if (listas.charAt(denun)=="'"){
          var tamaden=("denuncia"+String(j)).length
          var denun = listas.indexOf("denuncia"+String(j))+tamaden+4; 
        }
         for (i=denun;i<listas.length;i++){
           if (listas[i]=="'"){
              i=listas.length+2;
      
           }else{
             den=den+String(listas[i]);
          }
        
          
         }
        
        if (listas.charAt(lat1)=="'"){
          var tamalt=("latitud"+String(j)).length
          var lat1 = listas.indexOf("latitud"+String(j))+tamalt+4; 
        }
         for (i=lat1;i<listas.length;i++){
           if (listas[i]=="'"){
              i=listas.length+2;
      
           }else{
             lati=lati+String(listas[i]);
          }
        
          
         }

        if (listas.charAt(lng1)=="'"){
           var tamalng=("longitud"+String(j)).length
           var lng1 = listas.indexOf("longitud"+String(j))+tamalng+4; 
        }
        for (i=lng1;i<listas.length;i++){
           if (listas[i]=="'"){
              i=listas.length+2;
            }else{
             lngt=lngt+String(listas[i]);
          }
        
          
        }
           
           delis=delis.replace(/xd1/gi,'Ñ')
           var refew='<strong style="color:red;font-size:10px;font-family:Arial"> Delitos : '+delis+' - Preventivo N°: '+preve+'<br>'+'Fecha de Denuncia :'+den+'</strong>'+'<a href='+'/preventivos/seleccionar/'+idpreve+'/'+'> Ver Preventivo</a>'
           var refe= 'Delitos : '+delis+' - Prev.N°: '+preve+' - Fecha de Denuncia :'+den
                      var marcadores = new google.maps.Marker({
                    position: new google.maps.LatLng(lati,lngt),
                    map: map,
                    title: refe,
                    icon:  delis.indexOf("ROBO,")>-1? image+'delitospropiedad.png' : delis.indexOf("HOMICIDIO,")>-1? image+'delitoscontrapeople.png' : image+'delitoscontrahonor.png',
                    animation: google.maps.Animation.bound
                   });
          lati="";
          lngt="";
          preve="";
          idpreve="";
          den="";
          delis="";
              
              bindInfoWindow(marcadores, map, infoWindow, refew);

         
}
       
   function bindInfoWindow(marcadores, map, infoWindow, refe) {
        google.maps.event.addListener(marcadores, 'click', function() {
         infoWindow.setContent(refe);
         infoWindow.open(map, marcadores);
        });
         
     }
  
}
        

  
    
     

google.maps.event.addDomListener(window, 'load', initializen);
}
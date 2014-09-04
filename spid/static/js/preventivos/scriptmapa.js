  function mensajes(){
       $.msgBox({
       title:"Jefatura de Policia Chubut        Sistemas Informaticos Rawson", 
       content:"Programadores : Cabo 1° Ceballos Jaime A. Cabo Dorado Fernando E.",
       type:"info"});
      } 
      function format(input){
         var num = input.value.replace(/\./g,'');
         if(!isNaN(num)){
            if(num.length>0){
               num=num.substring(0,num.length-1)+num.substring(num.length-1);
            }
            if(num.length>8 ){
               alert('Ingrese el Nro de Dni sin puntos y hasta 8 digitos)');
                 num=num.substring(0,num.length-1)+num.substring(num.length-1)+'';
            }else{
               input.value = num;
            }
         }else{

          alert('Solo se permiten numeros(Ingrese el Nro de Dni sin puntos y hasta 8 digitos)');
             input.value ='';
         }
      }
      function isNumberKey(evt,input){
         var charCode = (evt.which) ? evt.which : event.keyCode
         var num = input.value.replace(/\./g,'');
        
         if (charCode > 31 && (charCode < 48 || charCode > 57))
            return false;
         if(num.length>7 ){
               alert('Ingrese el Nro de Dni sin puntos y hasta 8 digitos)');
               return false;
         }
         return true;
      }
      function isNumberKey1(evt){
         var charCode = (evt.which) ? evt.which : event.keyCode
        
         if (charCode > 31 && (charCode < 48 || charCode > 57))
            return false;
        
         return true;
      }
      function cambiar(valor){
        var toLoad;
        var valores = $('#idc').val();
                  
                    if (valores!=''){
                      toLoad= '../ids/'+valor+'/';
                    }else{
                      toLoad= 'ids/'+valor+'/';
        
                    }
       
 
        $.get(toLoad, function(data){
             var options = '<option value="">Seleccione Ciudad<option>';
             for (var i = 0; i < data.length; i++){
               options += '<option value="'+data[i]["pk"]+'">' +data[i]["fields"]["descripcion"] +'</option>'
             }
                          $('#calles').html(options)
                          $("#calles option:first").attr('selected', 'selected');
       }, "json");
     
      }
   
 
     
      
 
   
			$(document).ready(function() {

			 
        var lat = $('#lat').val();
        var lng = $('#longi').val();
        var latitud = $('#latitud').val();
        var longitud= $('#longitud').val();
        if(latitud != '' && latitud !='None' && longitud != '' && latitud !='None'){
          initializer(latitud,longitud);
        }else{  
           initializer(lat,lng);
        }
        
       
        
       
        $('#tipo_lugar').change(function(event){
            document.getElementById("datos_barrio").style.display='block'
            document.getElementById("datos_depe").style.display='none'
            var opcion = $('#tipo_lugar option:selected').text();
            if(opcion == 'DEPENDENCIA POLICIAL'){
              document.getElementById("datos_barrio").style.display='none'
              document.getElementById("datos_depe").style.display='block'
            }
        });

        $('#addbarrio').click(function(event){
            $("#nuevo_barrio").each(function() {
              displaying = $(this).css("display");
              if(displaying == "inline-block") {
                  $(this).css("display","none");
              } else {
                $(this).css("display","inline");
              }
            });
            $("#informacion2").each(function() {
              displaying = $(this).css("display");
              if(displaying == "block") {
                  $(this).css("display","none");
              } else {
                $(this).css("display","block");
              }
            });
            
        });
$('#cerrarinfo').click(function(evento) {
           $('#informacion').fadeOut(2000);
          });

        $('#pais_res').change(function(){
          var paisres= $(this).find(":selected").text();
          if (paisres=='ARGENTINA'){
            $('#domicilio').fadeIn(50);
          }else{
            $('#domicilio').fadeOut(50);
          }  
       

        });
         $('#tipo_lugar').change(function(event){
            document.getElementById("datos_barrio").style.display='block'
            document.getElementById("datos_depe").style.display='none'
            var opcion = $('#tipo_lugar option:selected').text();
            if(opcion == 'DEPENDENCIA POLICIAL'){
              document.getElementById("datos_barrio").style.display='none'
              document.getElementById("datos_depe").style.display='block'
            }
        });
       $('#buscar').click(function(evento){
          address = $('#calle option:selected').text() + ' ' + $('#altura').val()+ ', '+$('#cpp').val();
          alert(address)
          initializes(address);
        });
   
         
            $('#ureg').change(function(event){

                    $('#depe').html('<option value="">Seleccione Unidad Regional</option>');
                    if($('#ureg').val()){
                      var idure= $('#ureg').val();  
                    }
                    var toLoad;
                    toLoad= '../ure/'+idure+'/';
    
                    $.get(toLoad, function(data){
 
                            var options = '<option value="">Seleccione Unidad Regional</option>';
                             for (var i = 0; i < data.length; i++){
                              
                                options += '<option value="'+data[i]["pk"]+'">' +data[i]["fields"]["descripcion"] +'</option>'
                         
                            }
                     
                            $('#depe').html(options)
                            $("#depe option:first").attr('selected', 'selected');
                            
              }, "json");
           }); 
     
   $("#calle").select2({
               minimumInputLength: 1
        });
        $("#barrio").select2({
          minimumInputLength: 1
        });
        $("#dependencia").select2({
          
         });
         $("#depe").select2({
          
         });
        $("#ureg").select2({
          
         });
            });
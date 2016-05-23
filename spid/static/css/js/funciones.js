 
      function isnumero(evt,input){
         var charCode = (evt.which) ? evt.which : event.keyCode
         var num = input.value.replace(/\./g,'');

         if (charCode > 31 && (charCode < 48 || charCode > 57))
            return false;
         if(num.length>1 ){
              $('#invalidoed').fadeIn(100);
               return false;
         }
         return true;
      }
      function isNumberKey(evt,input){
         var charCode = (evt.which) ? evt.which : event.keyCode
         var num = input.value.replace(/\./g,'');
         
         if (charCode > 31 && (charCode < 48 || charCode > 57))
            return false;
         if(num.length>7 ){
               $('#invalido').fadeIn(100);
            
               return false;
         }
         return true;
      }
      function printDiv(divName) {
        var printContents = document.getElementById(divName).innerHTML;
        var originalContents = document.body.innerHTML;
        document.body.innerHTML = printContents;

        window.print();


        document.body.innerHTML = originalContents;
      }
     
      function printDiv(divName) {
        var printContents = document.getElementById(divName).innerHTML;
        var originalContents = document.body.innerHTML;
        document.body.innerHTML = printContents;

        window.print();


        document.body.innerHTML = originalContents;
      }
      function isNumberKey1(evt,input){
         var charCode = (evt.which) ? evt.which : event.keyCode
         var num = input.value.replace(/\./g,'');
        
         if (charCode > 31 && (charCode < 48 || charCode > 57))

            return false;
         if(num.length>10  ){
              $('#invalidoc').fadeIn(100);
               return false;
         }
         return true;
      }
   
      function validarEmail(valor) {
          var x = valor.value;
          var atpos = x.indexOf("@");
          var dotpos = x.lastIndexOf(".");
          if (x !=''){
            if (atpos< 1 || dotpos<atpos+2 || dotpos+2>=x.length) {
              $('#invalidoe').fadeIn(100);
              return false;
            }
          }
      }
 function isNumberKey2(evt,input){
         var charCode = (evt.which) ? evt.which : event.keyCode
         var num = input.value(/^\d{10}$/);
        
         if (charCode > 31 && (charCode < 48 || charCode > 57))
            return false;
         if(num.length>33 ){
             $('#invalidot').fadeIn(100);
               return false;
         }
         return true;
      }
    $(document).ready(function() {
        $.extend( $.fn.dataTable.defaults, {
            /*"bFilter": false,*/
            "bSort": false
        } );
     
        $('#example').dataTable();
        $('#tabs').tab();
        $("#addciudades").on('click',function(e){
        
            $("#oculto").fadeIn(200);

            $("#addpais").val($('#pais').val());
            $("#addprovi").val($('#provincia_id').val());
     
        });
         $("#addclose").on('click',function(e){
        
            $("#oculto").fadeOut(200);
             $("#addpais").val($('#pais').val());
            $("#addprovi").val($('#provincia_id').val());
       
        });
        $("#addbarrios").on('click',function(e){
            $("#ocultob").fadeIn(200);
            $("#addc").val($('#ciudad_res_id').val());
        });
         $("#addcloseb").on('click',function(e){
        
            $("#ocultob").fadeOut(200);
                $("#addc").val($('#ciudad_res_id').val());
       
        });

        $('#pais_id').on('click',function(e){
                   
                    $('#ciudad_res_id').html('<option value="">Seleccione Ciudad Residencia</option>');
                 
                    var idPais= $('#pais_id').val();
                    var valor = $('#ids').val();
                   
                    var toLoad;
                   
                     if (valor!='' ){
                       toLoad= '../../datap/'+idPais+'/';
                     }else{
                       toLoad= '../datap/'+idPais+'/';
                     }
               
                   $.get(toLoad, function(data){
                      var options = '<option value="">Seleccione Ciudad Residencia</option>';
                      
                            for (var i = 0; i < data.length; i++){
                              
                                options += '<option value="'+data[i]["pk"]+'">' +data[i]["fields"]["descripcion"] +'</option>'
                         
                            }
                            
                              $('#ciudad_res_id').html(options)
                            $("#ciudad_res_id option:first").attr('selected', 'selected');
                         
              }, "json");
           });
        $('#pais').click(function(event){
                 
                    $('#provincia_id').html('<option value="">Seleccione Provincias</option>');
                
                    $('#ciudad_nac_id').html('<option value="">Seleccione Ciudades</option>');
                 
                    var idPais= $('#pais').val();
                    var valor = $('#ids').val();
                   
                    var toLoad;

             
                     if (valor!='' ){
                       toLoad= '../../ciudades/data/'+idPais+'/';
                     }else{
                       toLoad= '../data/'+idPais+'/';
                     }
              
                   $.get(toLoad, function(data){
                      var options = '<option value="">Seleccione Provincia</option>';
                      $('#ciudad_nac_id').html('<option value="">Seleccione Ciudades</option>');
                      
                            for (var i = 0; i < data.length; i++){
                              
                                options += '<option value="'+data[i]["pk"]+'">' +data[i]["fields"]["descripcion"] +'</option>'
                         
                            }
                            
                              $('#provincia_id').html(options)
                            $("#provincia_id option:first").attr('selected', 'selected');
                             
                            $('#ciudad_nac_id').html(options)
                            $("#ciudad_nac_id option:first").attr('selected', 'selected');
                          
         
              }, "json");
           });
         $('#addpais').click(function(event){
                 
                  
                      $('#addprovi').html('<option value="">Seleccione Provincias</option>');
                  
                 
                    var idPais= $('#addpais').val();
                    var valor = $('#ids').val();
                   
                    var toLoad;

             
                     if (valor!='' ){
                       toLoad= '../../ciudades/data/'+idPais+'/';
                     }else{
                       toLoad= '../data/'+idPais+'/';
                     }
            
                   $.get(toLoad, function(data){
                      var options = '<option value="">Seleccione Provincia</option>';
                            for (var i = 0; i < data.length; i++){
                              
                                options += '<option value="'+data[i]["pk"]+'">' +data[i]["fields"]["descripcion"] +'</option>'
                         
                            }
                            
                     
                              $('#addprovi').html(options)
                            $("#addprovi option:first").attr('selected', 'selected');
                
         
              }, "json");
           });
        $('#provincia_id').click(function(event){
        
                  var idp= $('#provincia_id').val();
                  var valor = $('#ids').val();
                  var toLoad;
                  if (idp==''){
                     idp=0;
                  }
                  if (valor!='' ){
                      toLoad= '../../data/'+idp+'/';
                  }else{
                      toLoad= '../data/'+idp+'/';
                  }
               
                  
            
                  $.get(toLoad, function(data){

                        var options = '<option value="">Seleccione un Ciudad</option>';
                    
                            for (var i = 0; i < data.length; i++){
                              
                                options += '<option value="'+data[i]["pk"]+'">' +data[i]["fields"]["descripcion"] +'</option>'
                         
                            }
                            $('#ciudad_nac_id').html(options)
                            $("#ciudad_nac_id option:first").attr('selected', 'selected');
                        
                           

              }, "json");
        });
       $('#ciudad_res_id').click(function(event){
        
                  var idp= $('#ciudad_res_id').val();
                  var valor = $('#ids').val();
                  var toLoad;
                
                  if (valor!='' ){
                      toLoad= '../../villages/data/'+idp+'/';
                  }else{
                      toLoad= '../data/'+idp+'/';
                  }
                 
                  
            
                  $.get(toLoad, function(data){

                        var options = '<option value="">Seleccione un Barrio</option>';
                    
                            for (var i = 0; i < data.length; i++){
                              
                                options += '<option value="'+data[i]["pk"]+'">' +data[i]["fields"]["descripcion"] +'</option>'
                         
                            }
                            $('#barrio_id').html(options)
                            $("#barrio_id option:first").attr('selected', 'selected');
              }, "json");
        });

        $("#opt").change(function(event){
             $("#opt1").attr('checked',false);
             $("#reside").attr('disabled',true);
         
        });
        $("#opt1").change(function(event){
             $("#opt").attr('checked',false);
          
               $("#reside").attr('disabled',false);
           }); 
        $("#opt2").change(function(event){
             $("#opt3").attr('checked',false);
             $("#cual_plan").attr('disabled',false);
         
        });
        $("#opt3").change(function(event){
             $("#opt2").attr('checked',false);
          
               $("#cual_plan").attr('disabled',true);
                $("#cual_plan").val('')       
     
        });
        $("#opt4").change(function(event){
             $("#opt5").attr('checked',false);
             $("#cual_discapacidad").attr('disabled',false);
         
        });
        $("#opt5").change(function(event){
             $("#opt4").attr('checked',false);
             $("#cual_discapacidad").attr('disabled',true);
             $("#cual_discapacidad").val('')     
         });
         $("#opt6").change(function(event){
             $("#opt7").attr('checked',false);
             $("#cual_ocupacion").attr('disabled',false);
             $("#independiente").attr('disabled',false);
             $("#dependiente").attr('disabled',false);
             $("#independiente").attr('disabled',false);
             $("#dependiente").attr('disabled',false);
             $("#montofliar").attr('disabled',false);

        });
        $("#opt7").change(function(event){
             $("#opt6").attr('checked',false);
             $("#cual_ocupacion").attr('disabled',true);
             $("#independiente").attr('disabled',true);
             $("#dependiente").attr('disabled',true);
             $("#independiente").attr('checked',false);
             $("#dependiente").attr('checked',false);
             $("#montofliar").attr('disabled',false);
             $("#cual_ocupacion").val('')     
         });
     $('#addc').select2('val', '1049');
      
        
         $('#barrio_id').select2({
              
          });
         $('#estudios_id').select2({
              
          });
            $('#ciudad_nac_id').select2({ });
           
            $('#ciudad').select2({});
            $('#paisr_id').select2({});
            $('#provinciar_id').select2({});

           $('#datepicker').datepicker({});
          
} ); 

      
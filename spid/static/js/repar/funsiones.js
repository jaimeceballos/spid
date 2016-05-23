 
$(document).ready(function() {
        $.extend( $.fn.dataTable.defaults, {
            /*"bFilter": false,*/
            "bSort": false
        } );
     
        $('#example').dataTable();
       /* $('#calibre').html('<option value="">Seleccione Armas</option>');*/
             
        $("#tipoar").click(function(event){
                    var idta= $('#tipoar').val(); 
                    var valor = $('#ids').val(); 
                    var toLoad;
                    if (valor!='' ){
                       toLoad= '../../tipoars/'+idta+'/';
                    }else{
                        toLoad= '../tipoars/'+idta+'/';
                    }
                 
                    $.get(toLoad, function(data){
 
                      var options = '<option value="">Seleccione un Calibre</option>';
                      for (var i = 0; i < data.length; i++){
                          options += '<option value="'+data[i]["pk"]+'">' +data[i]["fields"]["descripcion"] +'</option>'
                      }
                   
                      $('#calibre').html(options)
                      $("#calibre option:first").attr('selected', 'selected');
                           
                    }, "json"); 
        });
        /*$('#modelo').html('<option value="">Seleccione Marca</option>');*/
             
        $("#marca").click(function(event){
                    var idma= $('#marca').val();  
                    var valor = $('#ids').val(); 
                    var toLoad;
                    if (valor!='' && valor!='None'){
                       toLoad= '../../marcas/'+idma+'/';
                    }else{
                        toLoad= '../marcas/'+idma+'/';
                    }
                   
                 
                    $.get(toLoad, function(data){
 
                      var options = '<option value="">Seleccione un Modelo</option>';
                      for (var i = 0; i < data.length; i++){
                          options += '<option value="'+data[i]["pk"]+'">' +data[i]["fields"]["descripcion"] +'</option>'
                      }
                      $('#modelo').html(options)
                      $("#modelo option:first").attr('selected', 'selected');
                           
                    }, "json"); 
        });
        $("#addmodels").on('click',function(e){
        
            $("#oculto").fadeIn(200);

               $("#addmodels").val($('#marca').val());
     
        });
        $("#addclose").on('click',function(e){
        
            $("#oculto").fadeOut(200);
               $("#addmodels").val($('#marca').val());
       
        });
         $("#searchpro").on('click',function(e){
        
            $("#protu").fadeIn(200);
        
     
        });
        $("#cierro").on('click',function(e){
        
            $("#protu").fadeOut(200);
            
       
        });
        $("#reset").on('click',function(e){
        
            $("#oculto").fadeOut(200);
            $("#marca").val($('#marca').val());
            $("form")[0].reset();
            $("#observaciones").val('');
        });
        $("#transf").on('click',function(e){
            $("#trans").fadeIn(200);
        });
        $("#cerro").on('click',function(e){
        
            $("#trans").fadeOut(200);
       
        });
         $("#seek").on('click',function(event){
                    var iddni= $('#datos').val(); 
                    if (iddni==''){
                       iddni='ZZ'
                    }
                    var idide= $('#ide').val(); 
                    var toLoad;
                
                    if (idide!='' && idide!=null){
                      toLoad = '../../new/'+iddni+'/';
                    }else{
                       toLoad= iddni+'/';
                    }
                    
                    $.get(toLoad, function(data){
 
                      var options = '<input value="">Seleccione un prontuario</option>';
                      if (data.length){
                        for (var i = 0; i < data.length; i++){
                            options += '<option value="'+data[i]["pk"]+'">' +data[i]["fields"]["n_c"]+',  Secc: '+data[i]["fields"]["tipo_p"] +', Pront. Nro: '+data[i]["fields"]["n_p"]+'</option>'
                        }
                      }else{

                          options = '<option value="">No se encontro coincidencia alguna</option>'
                  
                      }
                      $('#modelos').html(options)
                      $("#modelos option:first").attr('selected', 'selected');
                                         
                    }, "json"); 

        });
});
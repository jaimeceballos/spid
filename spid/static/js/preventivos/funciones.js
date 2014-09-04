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
      function isNumberKeyc(evt,input){
         var charCode = (evt.which) ? evt.which : event.keyCode
         var num = input.value.replace(/\./g,'');
        
         if (charCode > 31 && (charCode < 48 || charCode > 57))
            return false;
         if(num.length>3 ){
               alert('El tamaño no debe superar los 4 digitos)');
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
               alert('Ingrese el Nro de Dni sin puntos y hasta 8 digitos)');
               return false;
         }
         return true;
      }
      function isNumberKey1(evt,input){
         var charCode = (evt.which) ? evt.which : event.keyCode
         var num = input.value.replace(/\./g,'');
        
         if (charCode > 31 && (charCode < 48 || charCode > 57))
            return false;
         if(num.length>10 ){
               alert('Ingrese el Nro de Cuit sin puntos ni guiones y hasta 11 digitos)');
               return false;
         }
         return true;
      }
        function isNumberKey2(evt,input){
         var charCode = (evt.which) ? evt.which : event.keyCode
         var num = input.value.replace(/\./g,'');
        
         if (charCode > 31 && (charCode < 48 || charCode > 57))
            return false;
         if(num.length>99 ){
               alert('Ingrese el Nro de Telefonos sin puntos ni guiones y hasta 100 digitos)');
               return false;
         }
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
function documentVerify(){
         var nro_doc=document.getElementById('nro_doc').value

         
        if( !nro_doc && $('#tipo_doc option:selected').text()=='NO POSEE'){
         var fechaActual = new Date();
         var dni = fechaActual.getTime();
         $('#nro_doc').val(dni);
        }
        if($('#fecha_nac').val()!=''){
          var anioNac= $('#fecha_nac').val().substr($('#fecha_nac').val().length-4,$('#fecha_nac').val().length);
          var anio = new Date().getFullYear();
          var edad = anio-anioNac;
          if(edad < 18){
            $('#menor').val('si');
          }
        }else{
          $('#menor').val('no');
        }
        
}

      function validaPersonaInv(){
        var grabar = $('#grabar').val()
     
        if(grabar=='Guardar'){
           if($('#roles option:selected').text()=='DENUNCIANTE'){
              return valp();
          }
        }
        if(grabar == 'Grabar'){

          return valp();

        }
        
        return true;
        

      }
      function valp(){
        
            if($('#estado_civil').val()==''){
                 alert('Debe seleccionar Estado Civil.');
                 return false;
            }
            if($('#pais_nac').val()==''){
                 alert('Debe seleccionar pais de nacimiento.');
                 return false;
            }
            if($('#ciudad_nac').val()==''){
                 alert('Debe seleccionar Ciudad de nacimiento.');
                 return false;
            }
            
            if($('#pais_res').val()==''){
                 alert('Debe seleccionar pais de residencia.');
                 return false;
            }
            if($('#ciudades_r').val()==''){
                 alert('Debe seleccionar ciudad de residencia.');
                 return false;
            }
            
            if($('#ocupacion').val()==''){
                 alert('Debe seleccionar Ocupacion.');
                 return false;
            }
            if($('padre_apellidos').val()=='' || $('padre_nombres').val()=='' || $('madre_apellidos').val()=='' || $('madre_nombres').val()=='' ){
                 alert('Debe ingresar los datos de los padres.');
                 return false;
            }
            return true;
      }

+function ($) { "use strict";

  // TOOLTIP PUBLIC CLASS DEFINITION
  // ===============================

  var Tooltip = function (element, options) {
    this.type       =
    this.options    =
    this.enabled    =
    this.timeout    =
    this.hoverState =
    this.$element   = null

    this.init('tooltip', element, options)
  }

  Tooltip.DEFAULTS = {
    animation: true
  , placement: 'top'
  , selector: false
  , template: '<div class="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>'
  , trigger: 'hover focus'
  , title: ''
  , delay: 0
  , html: false
  , container: false
  }

  Tooltip.prototype.init = function (type, element, options) {
    this.enabled  = true
    this.type     = type
    this.$element = $(element)
    this.options  = this.getOptions(options)

    var triggers = this.options.trigger.split(' ')

    for (var i = triggers.length; i--;) {
      var trigger = triggers[i]

      if (trigger == 'click') {
        this.$element.on('click.' + this.type, this.options.selector, $.proxy(this.toggle, this))
      } else if (trigger != 'manual') {
        var eventIn  = trigger == 'hover' ? 'mouseenter' : 'focus'
        var eventOut = trigger == 'hover' ? 'mouseleave' : 'blur'

        this.$element.on(eventIn  + '.' + this.type, this.options.selector, $.proxy(this.enter, this))
        this.$element.on(eventOut + '.' + this.type, this.options.selector, $.proxy(this.leave, this))
      }
    }

    this.options.selector ?
      (this._options = $.extend({}, this.options, { trigger: 'manual', selector: '' })) :
      this.fixTitle()
  }

  Tooltip.prototype.getDefaults = function () {
    return Tooltip.DEFAULTS
  }

  Tooltip.prototype.getOptions = function (options) {
    options = $.extend({}, this.getDefaults(), this.$element.data(), options)

    if (options.delay && typeof options.delay == 'number') {
      options.delay = {
        show: options.delay
      , hide: options.delay
      }
    }

    return options
  }

  Tooltip.prototype.getDelegateOptions = function () {
    var options  = {}
    var defaults = this.getDefaults()

    this._options && $.each(this._options, function (key, value) {
      if (defaults[key] != value) options[key] = value
    })

    return options
  }

  Tooltip.prototype.enter = function (obj) {
    var self = obj instanceof this.constructor ?
      obj : $(obj.currentTarget)[this.type](this.getDelegateOptions()).data('bs.' + this.type)

    clearTimeout(self.timeout)

    self.hoverState = 'in'

    if (!self.options.delay || !self.options.delay.show) return self.show()

    self.timeout = setTimeout(function () {
      if (self.hoverState == 'in') self.show()
    }, self.options.delay.show)
  }

  Tooltip.prototype.leave = function (obj) {
    var self = obj instanceof this.constructor ?
      obj : $(obj.currentTarget)[this.type](this.getDelegateOptions()).data('bs.' + this.type)

    clearTimeout(self.timeout)

    self.hoverState = 'out'

    if (!self.options.delay || !self.options.delay.hide) return self.hide()

    self.timeout = setTimeout(function () {
      if (self.hoverState == 'out') self.hide()
    }, self.options.delay.hide)
  }

  Tooltip.prototype.show = function () {
    var e = $.Event('show.bs.'+ this.type)

    if (this.hasContent() && this.enabled) {
      this.$element.trigger(e)

      if (e.isDefaultPrevented()) return

      var $tip = this.tip()

      this.setContent()

      if (this.options.animation) $tip.addClass('fade')

      var placement = typeof this.options.placement == 'function' ?
        this.options.placement.call(this, $tip[0], this.$element[0]) :
        this.options.placement

      var autoToken = /\s?auto?\s?/i
      var autoPlace = autoToken.test(placement)
      if (autoPlace) placement = placement.replace(autoToken, '') || 'top'

      $tip
        .detach()
        .css({ top: 0, left: 0, display: 'block' })
        .addClass(placement)

      this.options.container ? $tip.appendTo(this.options.container) : $tip.insertAfter(this.$element)

      var pos          = this.getPosition()
      var actualWidth  = $tip[0].offsetWidth
      var actualHeight = $tip[0].offsetHeight

      if (autoPlace) {
        var $parent = this.$element.parent()

        var orgPlacement = placement
        var docScroll    = document.documentElement.scrollTop || document.body.scrollTop
        var parentWidth  = this.options.container == 'body' ? window.innerWidth  : $parent.outerWidth()
        var parentHeight = this.options.container == 'body' ? window.innerHeight : $parent.outerHeight()
        var parentLeft   = this.options.container == 'body' ? 0 : $parent.offset().left

        placement = placement == 'bottom' && pos.top   + pos.height  + actualHeight - docScroll > parentHeight  ? 'top'    :
                    placement == 'top'    && pos.top   - docScroll   - actualHeight < 0                         ? 'bottom' :
                    placement == 'right'  && pos.right + actualWidth > parentWidth                              ? 'left'   :
                    placement == 'left'   && pos.left  - actualWidth < parentLeft                               ? 'right'  :
                    placement

        $tip
          .removeClass(orgPlacement)
          .addClass(placement)
      }

      var calculatedOffset = this.getCalculatedOffset(placement, pos, actualWidth, actualHeight)

      this.applyPlacement(calculatedOffset, placement)
      this.$element.trigger('shown.bs.' + this.type)
    }
  }

  Tooltip.prototype.applyPlacement = function(offset, placement) {
    var replace
    var $tip   = this.tip()
    var width  = $tip[0].offsetWidth
    var height = $tip[0].offsetHeight

    // manually read margins because getBoundingClientRect includes difference
    var marginTop = parseInt($tip.css('margin-top'), 10)
    var marginLeft = parseInt($tip.css('margin-left'), 10)

    // we must check for NaN for ie 8/9
    if (isNaN(marginTop))  marginTop  = 0
    if (isNaN(marginLeft)) marginLeft = 0

    offset.top  = offset.top  + marginTop
    offset.left = offset.left + marginLeft

    $tip
      .offset(offset)
      .addClass('in')

    // check to see if placing tip in new offset caused the tip to resize itself
    var actualWidth  = $tip[0].offsetWidth
    var actualHeight = $tip[0].offsetHeight

    if (placement == 'top' && actualHeight != height) {
      replace = true
      offset.top = offset.top + height - actualHeight
    }

    if (/bottom|top/.test(placement)) {
      var delta = 0

      if (offset.left < 0) {
        delta       = offset.left * -2
        offset.left = 0

        $tip.offset(offset)

        actualWidth  = $tip[0].offsetWidth
        actualHeight = $tip[0].offsetHeight
      }

      this.replaceArrow(delta - width + actualWidth, actualWidth, 'left')
    } else {
      this.replaceArrow(actualHeight - height, actualHeight, 'top')
    }

    if (replace) $tip.offset(offset)
  }

  Tooltip.prototype.replaceArrow = function(delta, dimension, position) {
    this.arrow().css(position, delta ? (50 * (1 - delta / dimension) + "%") : '')
  }

  Tooltip.prototype.setContent = function () {
    var $tip  = this.tip()
    var title = this.getTitle()

    $tip.find('.tooltip-inner')[this.options.html ? 'html' : 'text'](title)
    $tip.removeClass('fade in top bottom left right')
  }

  Tooltip.prototype.hide = function () {
    var that = this
    var $tip = this.tip()
    var e    = $.Event('hide.bs.' + this.type)

    function complete() {
      if (that.hoverState != 'in') $tip.detach()
    }

    this.$element.trigger(e)

    if (e.isDefaultPrevented()) return

    $tip.removeClass('in')

    $.support.transition && this.$tip.hasClass('fade') ?
      $tip
        .one($.support.transition.end, complete)
        .emulateTransitionEnd(150) :
      complete()

    this.$element.trigger('hidden.bs.' + this.type)

    return this
  }

  Tooltip.prototype.fixTitle = function () {
    var $e = this.$element
    if ($e.attr('title') || typeof($e.attr('data-original-title')) != 'string') {
      $e.attr('data-original-title', $e.attr('title') || '').attr('title', '')
    }
  }

  Tooltip.prototype.hasContent = function () {
    return this.getTitle()
  }

  Tooltip.prototype.getPosition = function () {
    var el = this.$element[0]
    return $.extend({}, (typeof el.getBoundingClientRect == 'function') ? el.getBoundingClientRect() : {
      width: el.offsetWidth
    , height: el.offsetHeight
    }, this.$element.offset())
  }

  Tooltip.prototype.getCalculatedOffset = function (placement, pos, actualWidth, actualHeight) {
    return placement == 'bottom' ? { top: pos.top + pos.height,   left: pos.left + pos.width / 2 - actualWidth / 2  } :
           placement == 'top'    ? { top: pos.top - actualHeight, left: pos.left + pos.width / 2 - actualWidth / 2  } :
           placement == 'left'   ? { top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left - actualWidth } :
        /* placement == 'right' */ { top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left + pos.width   }
  }

  Tooltip.prototype.getTitle = function () {
    var title
    var $e = this.$element
    var o  = this.options

    title = $e.attr('data-original-title')
      || (typeof o.title == 'function' ? o.title.call($e[0]) :  o.title)

    return title
  }

  Tooltip.prototype.tip = function () {
    return this.$tip = this.$tip || $(this.options.template)
  }

  Tooltip.prototype.arrow = function () {
    return this.$arrow = this.$arrow || this.tip().find('.tooltip-arrow')
  }

  Tooltip.prototype.validate = function () {
    if (!this.$element[0].parentNode) {
      this.hide()
      this.$element = null
      this.options  = null
    }
  }

  Tooltip.prototype.enable = function () {
    this.enabled = true
  }

  Tooltip.prototype.disable = function () {
    this.enabled = false
  }

  Tooltip.prototype.toggleEnabled = function () {
    this.enabled = !this.enabled
  }

  Tooltip.prototype.toggle = function (e) {
    var self = e ? $(e.currentTarget)[this.type](this.getDelegateOptions()).data('bs.' + this.type) : this
    self.tip().hasClass('in') ? self.leave(self) : self.enter(self)
  }

  Tooltip.prototype.destroy = function () {
    this.hide().$element.off('.' + this.type).removeData('bs.' + this.type)
  }


  // TOOLTIP PLUGIN DEFINITION
  // =========================

  var old = $.fn.tooltip

  $.fn.tooltip = function (option) {
    return this.each(function () {
      var $this   = $(this)
      var data    = $this.data('bs.tooltip')
      var options = typeof option == 'object' && option

      if (!data) $this.data('bs.tooltip', (data = new Tooltip(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  $.fn.tooltip.Constructor = Tooltip


  // TOOLTIP NO CONFLICT
  // ===================

  $.fn.tooltip.noConflict = function () {
    $.fn.tooltip = old
    return this
  }

}(window.jQuery);

$(document).ready(function() {
      
 
        $('#example').dataTable( {
                  "aaSorting": [[ 2 , "asc" ]]
                  } );
        $('#examples').dataTable( {
                  "aaSorting": [[ 1 , "asc" ]]
                  } );
        $("[rel='tooltip']").tooltip();
        $('#roles').change(function(event){
           var options= $(this).find(":selected").text();
         
           if (options=='APREHENDIDO' || options=='APRENDIDO' || options=='DETENIDO'){
              $('#detenidos').fadeIn(50);
              $('#razon').fadeOut(50);
              $('#menores').fadeOut(50);
            
           }else{
             if (options=='DENUNCIANTE'){
                $('#razon').fadeIn(50);
                $('#detenidos').fadeOut(50);
                $('#menores').fadeOut(50);
                $('#esdetenido').fadeOut(50);
    
             }else{
              if (options=='DENUNCIADO' || options=='VICTIMA'){
                $('#menores').fadeIn(50);
                $('#razon').fadeIn(50);
                $('#detenidos').fadeOut(50);
                $('#esdetenido').fadeOut(50);
    
              }else{
                $('#detenidos').fadeOut(50);
                $('#razon').fadeOut(50);
                $('#menores').fadeIn(50);
                $('#esdetenido').fadeOut(50);
    
              } 
             } 
      
           }   
    
        });
        $('#todo').change(function(event){
           
            opciones = document.getElementsByName("ciudades");
            
            
            if($(this).attr("checked")=="checked"){
              for(var i=0; i<opciones.length;i++) {
                
               
                $('#id_ciudades_'+i).attr('checked', true);
              }
            }else{
            
             for(var i=0; i<opciones.length;i++) {
                
                
                $('#id_ciudades_'+i).attr('checked',false);
              }
            }
      
        });
 $("#ciudades").select2({
          
         });
        $("#ciudad_nac").select2({
          
         });
         $("#nro-unidad").select2({
          
         });
           $("#ureg").select2({
          
         });
         $('#tipo').select2({});
         $('#unidadmed').select2({});
         $('#subtipos').select2({});
        $('#sistema_disparo').select2({});
        $('#tipo').select2({});
        $('#categorias').select2({  minimumInputLength: 1});
         $('#id_actores-actuante').select2({minimumInputLength: 1});
        $('#id_actores-preventor').select2({minimumInputLength: 1});
        $('#marcas').select2({  minimumInputLength: 1});
        $('#ciudades_r').select2({ });
        $("#permissions").select2({});
        $('#idmarca').select2({
              minimumInputLength: 1
          });
        $("#calle").select2({
          
        });
        $("#calles").select2({
          
        });
        $("#barrio_codigo").select2({
          
        });
        $("#entre").select2({
          
        });
        $("#barrio").select2({
          
        });
        $("#dependencia").select2({});
    

     
        $("#depe").select2({
          
         });
        $('#ciudad').select2({
              minimumInputLength: 1
          });
       
        $("#mes").select2({})
        $("#anios").select2({})
        $("#tipodel").select2({})
        $("#delitoe").select2({})
       
        $("#provi").change(function(event){

          if ($(this).attr("checked")=="checked"){
             $("#depes").attr('checked',false);
             $("#ciu").attr('checked',false);
             $("#combodepe").fadeOut(200)
             $("#combociu").fadeOut(200)
             $("#vista").fadeIn(200)
             $("#reportes").fadeOut(200)
             
           }else{
             $("#depes").attr('checked',false);
             $("#ciu").attr('checked',false);
             $("#combodepe").fadeOut(200)
             $("#combociu").fadeOut(200)
             $("#vista").fadeOut(200)
             $("#reportes").fadeOut(200)
           }
         
        });
         

          $("#ciu").change(function(event){

          if ($(this).attr("checked")=="checked"){
             $("#depes").attr('checked',false);
             $("#provi").attr('checked',false);
             $("#combodepe").fadeOut(200)
             $("#combociu").fadeIn(200)
             $("#combofechas").fadeIn(200)
             $("#vista").fadeOut(200)
             
           }else{
             $("#depes").attr('checked',false);
             $("#provi").attr('checked',false);
             $("#combodepe").fadeOut(200)
             $("#combociu").fadeOut(200)
             $("#combofechas").fadeOut(200)
   
           }
         
        });
            $("#vere").click(function(event){
               $("#verele").fadeIn(100)
            });
            $("#cancelar").click(function(event){
               $("#verele").fadeOut(100)
            });
            $("#verper").click(function(event){
               $("#verpers").fadeIn(100)
            });
            $("#cancelarp").click(function(event){
               $("#verpers").fadeOut(100)
            });
        $("#depes").change(function(event){
          if ($(this).attr("checked")=="checked"){
             $("#ciu").attr('checked',false);
             $("#provi").attr('checked',false);
             $("#combodepe").fadeIn(200)
             $("#combociu").fadeOut(200)
             $("#combofechas").fadeIn(200)
             $("#vista").fadeOut(200)
             $("#reportes").fadeOut(200)
           }else{
             $("#ciu").attr('checked',false);
             $("#provi").attr('checked',false);
             $("#combodepe").fadeOut(200)
             $("#combociu").fadeOut(200)
             $("#combofechas").fadeOut(200)
             $("#reportes").fadeOut(200)
           }
         
        }); 
        
         $('#tipos').select2({}).change(function(event){
                    $('#subtipos').html('<option value="">Seleccione Tipo de uso de Arma de Fuego</option>');
                    var ida = $('#idampl').val();
                    var idelemento = $('#idele').val();
                    var uso = $('#tipos').val();
                    var toLoad;
                    var options=''
                    
                    if (ida==null){
                       toLoad= '../../modouso/'+uso+'/';
                    }else{
                    
                       toLoad= '../../../modouso/'+uso+'/';
                     }
             
                 
                    $.get(toLoad, function(data){
 
                             for (var i = 0; i < data.length; i++){
                              
                                options += '<option value="'+data[i]["pk"]+'">' +data[i]["fields"]["descripcion"] +'</option>'
                         
                            }
                      
                            $('#subtipos').html(options)
                            $("#subtipos option:first").attr('selected', 'selected');
              }, "json");
           });  
       
        $('#categoria').select2({}).change(function(evento) {
           var dfuego=$('#categoria option:selected').text();
            if (dfuego=='DE FUEGO' || dfuego=='FUEGO'){
                alert('A continuacion debe cargar las caracteristicas generales del Arma de fuego')
        
                $('#habilitaf').fadeIn(500);
           }else{
                $('#habilitaf').fadeOut(500);
          }
        });
         
        $('#rubro').select2({}).change(function(event){
                    $('#habilitaf').fadeOut(500);
                    var ida=$('#idampl').val();
                    var rubro = $('#rubro').val();
                    var idelemento = $('#idele').val();
                    var toLoad;
                    var options=''
                    
                   
                    if (ida==null){
                      toLoad= '../../getcategory/'+rubro+'/';
                    }else{
                       toLoad= '../../../getcategory/'+rubro+'/';
                    }
               
                   $.get(toLoad, function(data){
                                  
                            for (var i = 0; i < data.length; i++){
                                
                               options += '<option value="'+data[i]["pk"]+'">' +data[i]["fields"]["descripcion"] +'</option>'
                              
                            }
                            
                            $('#categoria').html(options)
                            $("#categoria option:first").attr('selected', 'selected');
                  }, "json"); 
                   var vehiculos=$('#rubro option:selected').text();
                    if (vehiculos=='VEHICULOS' || vehiculos=='AUTOMOTORES'){
                        alert('A continuacion debe cargar las caracteristicas generales del Vehiculo '+$('#tipo option:selected').text())
        
                        $('#habilitav').fadeIn(500);
                    }else{
                         $('#habilitav').fadeOut(500);
                  }
           });
       

       
        
        

 $('#ciudades_r').change(function(event){
                    var idcit= $('#ciudades_r').val();
                    var valor = $('#ids').val();
                    var toLoad;
                    var options = '<option value="">Seleccione Barrio</option>';
             
                    if (valor!='' && valor!='None'){
                      toLoad= '../../town/'+idcit+'/';
                    }else{
                      toLoad= 'town/'+idcit+'/';
                    }
                 
                   $.get(toLoad, function(data){
                                  
                            for (var i = 0; i < data.length; i++){
                                
                               options += '<option value="'+data[i]["pk"]+'">' +data[i]["fields"]["descripcion"] +'</option>'
                              
                            }
                            
                            $('#barrio_codigo').html(options)
                            $("#barrio_codigo option:first").attr('selected', 'selected');
                  }, "json"); 
                   var options2 = '<option value="">Seleccione calle</option>';
                   if (valor!='' && valor!='None'){
                      toLoad= '../../street/'+idcit+'/';
                    }else{
                      toLoad = 'street/'+idcit+'/';
                    }
                   $.get(toLoad, function(data){
                      for (var i = 0; i < data.length; i++){
                        options2 += '<option value="'+data[i]["pk"]+'">' +data[i]["fields"]["descripcion"] +'</option>'
                      }
                           
                           
                          $('#calles').html(options2)
                            $("#calles:first").attr('selected', 'selected');
                            $('#entre').html(options2)
                            $("#entre:first").attr('selected', 'selected');
                   },"json");
           });
        $('#tipodel').change(function(event){
                    $('#delitoe').html('<option value="">Seleccione Tipos de Delitos</option>');
                    var idtd= $('#tipodel').val();
                    var toLoad;
              
                   
                    toLoad=idtd+'/';
               
                    $.get(toLoad, function(data){
                          
                            if (data.length!=0){
                               var options = '<option value="">Seleccione Delitos</option>';
                            }else{
                               var options = '<option value=""></option>';
                            }
                             for (var i = 0; i < data.length; i++){
                              
                                options += '<option value="'+data[i]["pk"]+'">' +data[i]["fields"]["descripcion"] +'</option>'
                         
                            }
                           
                            $('#delitoe').html(options)
                            $("#delitoe option:first").attr('selected', 'selected');
              }, "json");
           });
        $('#tipodelito').change(function(event){
                    $('#delito').html('<option value="">Seleccione Tipos de Delitos</option>');
                    $('#modos').html('<option value="">Seleccione Delitos</option>');

                    var idtd= $('#tipodelito').val();
                    var toLoad;
              
                   
                    toLoad= '../tdelito/'+idtd+'/';
                   
                    $.get(toLoad, function(data){
                            if (data.length!=0){
                               var options = '<option value="">Seleccione Delitos</option>';
                            }else{
                               var options = '<option value=""></option>';
                            }
                             for (var i = 0; i < data.length; i++){
                              
                                options += '<option value="'+data[i]["pk"]+'">' +data[i]["fields"]["descripcion"] +'</option>'
                         
                            }
                      
                            $('#delito').html(options)
                            $("#delito option:first").attr('selected', 'selected');
              }, "json");
           });
        $('#delito').change(function(event){
                    $('#modos').html('<option value="">Seleccione Delitos</option>');
                   

                    var idtd= $('#delito').val();
                    var toLoad;
               
                    toLoad= '../delito/'+idtd+'/';
                    
                    $.get(toLoad, function(data){
                             if (data.length!=0){var options = '<option value="">Seleccione Modos Aquí</option>';
                             }else{
                               var options = '<option value="">Modos solo con LESIONES</option>';
                             }  
                             for (var i = 0; i < data.length; i++){
                              
                                options += '<option value="'+data[i]["pk"]+'">' +data[i]["fields"]["descripcion"] +'</option>'
                         
                            }
                      
                            $('#modos').html(options)
                            $("#modos option:first").attr('selected', 'selected');
         
              }, "json");
           });
          
            $('#ureg').change(function(event){
                   
                    $('#depe').html('<option value="">Seleccione Unidad Regional</option>');
                    if($('#ureg').val()){
                      var idure= $('#ureg').val();  
                    }else{
                      var idure= $('#nro-unidad').val();
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
     
       $('#nro-unidad').change(function(event){
                    $('#depe').html('<option value="">Seleccione Unidad Regional</option>');
                    if($('#ureg').val()){
                      var idure= $('#ureg').val();  
                    }else{
                      var idure= $('#nro-unidad').val();
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
       
    
       
        $('#addmarca').click(function(event){

          $("#nueva_marca").each(function() {
              displaying = $(this).css("display");
              if(displaying == "inline-block") {
                  $(this).css("display","none");
              } else {
                $(this).css("display","inline");
              }
            });

        });
         $('#addmarcav').click(function(event){
          
          $("#nueva_marcav").each(function() {
              displaying = $(this).css("display");
              if(displaying == "inline-block") {
                  $(this).css("display","none");
              } else {
                $(this).css("display","inline");
              }
            });

        });  

       $("#ciu").change(function(event){

          if ($(this).attr("checked")=="checked"){
             $("#depes").attr('checked',false);
             $("#combodepe").fadeOut(200)
             $("#combociu").fadeIn(200)
             $("#combofechas").fadeIn(200)
             
           }else{
             $("#depes").attr('checked',false);
             $("#combodepe").fadeOut(200)
             $("#combociu").fadeOut(200)
              $("#combofechas").fadeOut(200)
           }
         
        });
        $("#depes").change(function(event){
          if ($(this).attr("checked")=="checked"){
             $("#ciu").attr('checked',false);
             $("#combodepe").fadeIn(200)
             $("#combociu").fadeOut(200)
              $("#combofechas").fadeIn(200)
           }else{
             $("#ciu").attr('checked',false);
             $("#combodepe").fadeOut(200)
             $("#combociu").fadeOut(200)
              $("#combofechas").fadeOut(200)
           }
         
        }); 
         
        $('#pais').change(function(event){
                  $('#provincia').html('<option value="">Seleccione Provincia</option>');
                  $('#departamento').html('<option value="">Seleccione Provincia</option>');
                  $('#ciudades').html('<option value="">Seleccione Ciudades</option>');
                
                    var idPais= $('#pais').val();
                    var valor = $('#ids').val();
                    var toLoad;
                    if (valor!='' && valor!='None'){
                      toLoad= '../../'+idPais+'/';
                    }else{
                      toLoad= idPais+'/';
        
                    }
                    
                   $.get(toLoad, function(data){
                      var options = '<option value="">Seleccione Provincia</option>';
                      $('#departamento').html('<option value="">Seleccione Provincia</option>');
                      $('#ciudades').html('<option value="">Seleccione Ciudades</option>');
                      
                            for (var i = 0; i < data.length; i++){
                              
                                options += '<option value="'+data[i]["pk"]+'">' +data[i]["fields"]["descripcion"] +'</option>'
                         
                            }
                            
                              $('#provincia').html(options)
                            $("#provincia option:first").attr('selected', 'selected');
                            $('#ciudades').html(options)
                            $("#ciudades option:first").attr('selected', 'selected');
              }, "json");
           });

  $('#pais_res').change(function(event){
                     $('#ciudades_r').html('<option value="">Seleccione Ciudad</option>');
                    var idPais= $('#pais_res').val();
                    var valor = $('#ids').val();
                    var toLoad;

                    if (valor!=''){
                      toLoad= '../../'+idPais+'/';
                    }else{
                      toLoad= idPais+'/';
          
                    }
                   
                   $.get(toLoad, function(data){
                            var options = '<option value="">Seleccione Ciudad</option>';
                             for (var i = 0; i < data.length; i++){
                              
                                options += '<option value="'+data[i]["pk"]+'">' +data[i]["fields"]["descripcion"] +'</option>'
                         
                            }
                      
                             $('#ciudades_r').html(options)
                            $("#ciudades_r option:first").attr('selected', 'selected');
              }, "json");
           });

           $('#provincia').change(function(event){
        
          var idp= $('#provincia').val();
          var valor = $('#ids').val();
                    var toLoad;
                    if (valor!=''){
                      toLoad= '../../dpto/'+idp+'/';
                    }else{
                      toLoad= 'dpto/'+ idp+'/';
                  }    
                  $.get(toLoad, function(data){

                        var options = '<option value="">Seleccione un Dpto</option>';
                    
                            for (var i = 0; i < data.length; i++){
                              
                                options += '<option value="'+data[i]["pk"]+'">' +data[i]["fields"]["descripcion"] +'</option>'
                         
                            }
                            $('#departamento').html(options)
                            $("#departamento option:first").attr('selected', 'selected');
              }, "json");
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
         $('#seekper').click(function(evento) {
           $('#buscarper').fadeIn(200);
          });
        $('#cerrarinfo').click(function(evento) {
           $('#informacion').fadeOut(2000);
           $('#buscarper').fadeOut(200);
          });

        $('#pais_res').change(function(){
          var paisres= $(this).find(":selected").text();
          if (paisres=='ARGENTINA'){
            $('#domicilio').fadeIn(50);
          }else{
            $('#domicilio').fadeOut(50);
          }  
       

        });
        $('#detenido').change(function(){
           var estadetenido= $('#detenido').val();
              if (estadetenido=='si'){
                $('#esdetenido').fadeIn(50);
                $('#razon').fadeOut(50);
              }else{
                $('#esdetenido').fadeOut(50);
                $('#razon').fadeIn(50); 
              }  
        });
       $('#buscar').click(function(evento){
          address = $('#calle option:selected').text() + ' ' + $('#altura').val()+ ', '+$('#cpp').val();
          alert(address)
          initializes(address);
        });



            });
 
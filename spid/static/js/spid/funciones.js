$(function() { 
	var emailreg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;	
	$(".botonAcceder").click(function(){  
		$(".error").fadeOut().remove();
		
        if ($(".name").val() == "") {  
			$(".name").focus().after('<span class="error">Ingrese Apellido y Nombre/s</span>');  
			return false;  
		}  
		if ($(".docu").val() == null || $(".docu").val().length == 0 ) {
            $(".docu").focus().after('<span class="error">Ingrese un nro. de Documento válido</span>');  
			return false;  
		}
		if ($(".jerarca").val() == "") {  
			$(".jerarca").focus().after('<span class="error">Ingrese Jerarquia</span>');  
			return false;  
		} 
		if ($(".destino").val() == "") {  
			$(".destino").focus().after('<span class="error">Ingrese Destino Actual</span>');  
			return false;  
		}  
        if ($(".mail").val() == "" || !emailreg.test($(".mail").val())) {
        
			$(".mail").focus().after('<span class="error">Ingrese un email correcto</span>');  
			return false;  
		}  
        if ($(".modif02").val() == "") {  
			$(".modif02").focus().after('<span class="error">Ingrese los usuarios y demas datos requeridos</span>');  
			return false;  
		}  
       
	
    });  
	$(".name").bind('blur keyup', function(){  
        if ($(this).val() != ""  ) {  			
			$('.error').fadeOut();
			return false;  
		}  
	});	
	$(".docu,").bind('blur keyup', function(){  
        if ($(this).val() != "" || $(this).val().length == 0 ) {  			
			$('.error').fadeOut();
			return false;  
		}  
	});	
	$(".jerarca").bind('blur keyup', function(){  
        if ($(this).val() != "" ) {  			
			$('.error').fadeOut();
			return false;  
		}  
	});	
	$(".destino").bind('blur keyup', function(){  
        if ($(this).val() != "" ) {  			
			$('.error').fadeOut();
			return false;  
		}  
	});	
	$(".mail").bind('blur keyup', function(){  
        if ($(".mail").val() != "" && emailreg.test($(".mail").val())) {	
			$('.error').fadeOut();  
			return false;  
		}  
	});
	$(".modif02").bind('blur keyup', function(){  
        if ($(this).val() != "" ) {  			
			$('.error').fadeOut();
			return false;  
		}  
	});	
})(jQuery);
jQuery(function ($) {
	
   $('#basic-modal .basic').click(function (e) {
		$('#contenido').modal();

		return false;
	});
   $('#basic-modal2 .basic').click(function (e) {
		$('#contenidos').modal();

		return false;
	});
    $('#basic-modal3 .basic').click(function (e) {
		$('#modificar').modal();

		return false;
	});
	$('#basic-modalcr .basic').click(function (e) {
		$('#ciudadres').modal();

		return false;
	});

   
      

});

$(document).ready(function(){
    $(".menu > li").click(function(e){
        var a = e.target.id;
        //desactivamos seccion y activamos elemento de menu
        $(".menu li.active").removeClass("active");
        $(".menu #"+a).addClass("active");
        //ocultamos divisiones, mostramos la seleccionada
        $(".content").css("display", "none");
        $("."+a).fadeIn();
    });
});
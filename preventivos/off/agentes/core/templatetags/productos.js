require('doff.template.base', 'Library');
require('agentes.core.models', 'Categoria', 'Producto');

register = new Library();
function categorias() {
    var categorias = Categoria.objects.filter({ super__isnull: true });
    return { "categorias": categorias };
}

register.inclusion_tag("categorias.html")(categorias);

function novedades(context) {
    var novedades = Producto.objects.order_by('-pk').slice(0, 5)
    return { "novedades": novedades, 'MEDIA_URL': context['MEDIA_URL'] };
}

register.inclusion_tag("novedades.html")(novedades, { takes_context: true});

publish({
	register: register
});
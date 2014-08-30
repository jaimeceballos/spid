require('agentes.core.models', 'Categoria', 'Producto');
require('doff.utils.shortcuts', 'get_object_or_404', 'render_to_response');
require('doff.template.context', 'RequestContext');

function productos_por_categoria(request, categoria) {
    var supercategoria = get_object_or_404(Categoria, { id: categoria, super__isnull: true});
    function lista_categorias(sup) {
        var subcategorias = sup.categoria_set.all();
        var resultado = [sup];
        for (var categoria in subcategorias)
        	resultado = resultado.concat(lista_categorias(categoria));
        return resultado;
    }
    var categorias = lista_categorias(supercategoria);
    categorias = categorias.filter(function(c) { return c.producto_set.count() > 0; });
    return render_to_response('productos.html', {'categorias': categorias}, new RequestContext(request));  
}

publish({ 
	productos_por_categoria: productos_por_categoria,
});

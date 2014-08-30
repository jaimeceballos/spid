// Top level offline url-to-view mapping.
require('doff.conf.urls', '*');

var urlpatterns = patterns('',
    ['^/?$', 'doff.views.generic.simple.direct_to_template', {'template': 'index.html'} ],
    ['^catalogo/$', 'doff.views.generic.simple.direct_to_template', {'template': 'catalogo.html'} ],
    ['^catalogo/categoria/(\\d+)/$', 'agentes.core.views.productos_por_categoria'],
    ['^catalogo/categoria/(\\d+)/$', 'agentes.core.catalogo.productos_por_categoria'],
    ['^catalogo/buscar/$', 'agentes.core.catalogo.buscar_productos'],
    ['^administrar/', include('agentes.core.urls')],
    ['^pedido/agregar/(\\d+)/$', 'agentes.ventas.views.agregar_producto'],
    ['^pedido/modificar/$', 'agentes.ventas.views.modificar_pedido'],
    ['^ventas', include('agentes.ventas.urls')]
)

// Don't touch this line
publish({ 
    urlpatterns: urlpatterns 
});

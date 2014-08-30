// Top level offline url-to-view mapping.

require('doff.conf.urls', '*');
require('agentes.ventas.models', 'Pedido');

var urlpatterns = patterns('',
        ['^/?$', 'doff.views.generic.simple.direct_to_template', {'template': 'ventas/index.html'} ],
        ['pedido/$', 'doff.views.generic.simple.redirect_to', {'url':'/ventas/pedidos/'}],
        ['pedido/(\d{1,5})/edit/$', 'agentes.ventas.views.edit_pedido',{}],
        ['pedidos/$', 'doff.views.generic.list_detail.object_list',{
            'queryset': Pedido.objects.all()
            }
        ],
        ['pedidos/add/$', 'doff.views.generic.simple.redirect_to', 
            {'url': '../../pedido/add/'}],
        ['pedido/add/$', 'agentes.ventas.views.create_pedido', ],
        ['pedido/(\d{1,5})/delete/$', 'doff.views.generic.create_update.delete_object', {
            'model': Pedido,
            'post_delete_redirect': '/ventas/pedidos/',
            'template_name': 'confirm_delete.html'}]
)

// Don't touch this line
publish({ 
    urlpatterns: urlpatterns 
});

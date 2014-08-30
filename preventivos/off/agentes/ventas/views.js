require('doff.utils.http', 'HttpResponseRedirect');
require('doff.utils.shortcuts', 'get_object_or_404', 'render_to_response');
require('agentes.ventas.forms', 'PedidoConItemsForm', 'PedidoForm');

function create_pedido(request, object_id) {
    var arg = new Arguments(arguments);
    if (request.method == "POST") {
        var form = new PedidoForm({data: request.POST});
        if (form.is_valid()) {
            var pedido = form.save();
            var pedido_id = pedido.id;
            var formset = new PedidoConItemsForm({data: request.POST, instance: pedido});
            if (formset.is_valid())
                var instances = formset.save();
                // Una vez creado por primera vez, se redirecciona al edit
                if (!object_id)
                    return new HttpResponseRedirect('../%d/edit/'.subs(pedido_id));
        } else {
            var formset = new PedidoConItemsForm();
        }
    } else {
        var form = new PedidoForm();
        var formset = new PedidoConItemsForm();
    }
    
    return render_to_response('ventas/pedido_form.html', {form: form, formset: formset});
}

function edit_pedido(request, object_id) {
    var pedido = get_object_or_404(Pedido, { id: object_id});
    if (request.method == "POST") {
        var form = new PedidoForm({data: request.POST, instance: pedido});
        if (form.is_valid())
            var pedido = form.save();
        
        var formset = new PedidoConItemsForm({data: request.POST, instance: pedido});
        if (formset.is_valid()) {
            var instances = formset.save();
            if ('save' in request.POST)
                return HttpResponseRedirect('../..');
            else
                var formset = new PedidoConItemsForm({ instance: pedido });
        }
    } else {
        var form = new PedidoForm({ instance: pedido });
        var formset = new PedidoConItemsForm({ instance: pedido });
    }
    return render_to_response('salesman/pedido_form.html', {form: form, formset: formset});
}

publish({
    create_pedido: create_pedido,
    edit_pedido: edit_pedido
});
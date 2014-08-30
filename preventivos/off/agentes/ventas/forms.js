require('doff.forms.models', 'ModelForm', 'inlineformset_factory');
require('agentes.ventas.models', 'Pedido', 'ItemPedido');

var PedidoForm = new type('PedidoForm', [ ModelForm ], { 
    Meta: { model: Pedido }
});

var PedidoConItemsForm = inlineformset_factory(Pedido, ItemPedido, { extra: 10 });

publish({
    PedidoForm: PedidoForm,
    PedidoConItemsForm: PedidoConItemsForm
});
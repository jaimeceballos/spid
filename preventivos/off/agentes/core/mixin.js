var Categoria = {
    __str__: function() {
        return this.super != null ? "%s - %s".subs(string(this.super), this.nombre) : this.nombre;
    }
};

var Producto = {
    __str__: function() {
        return this.nombre;
    }
};

publish({
	Categoria: Categoria,
	Producto: Producto
});
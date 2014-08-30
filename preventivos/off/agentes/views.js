require('doff.utils.http', '*');
require('doff.template.loader');
require('doff.template.context', 'Context');

function index(request){

    var c = new Context();
    var t = loader.get_template('index.html');
    return new HttpResponse(t.render(c));
}

publish({ 
    index: index,
});

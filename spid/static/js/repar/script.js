function __init()
{

    $('#search_input')
        .val('')
        .focus()
        .keyup(function(){

            if(!$.trim($(this).val()))
                $('.results .error').empty().hide();
        });
      
    var cache = {};
    $('#search_input').autocomplete({
        minLength: 2,
        select: function( event, ui ) {
            return false;
        },

        open: function() {
            $('.results .wrapper').html($(this).autocomplete("widget").html());
            $(this).autocomplete("widget").hide();
        },
        source: function( request, response ) {

            if (cache[request.term]) {
                response(cache[request.term]);
                return;
            }

            $.ajax({
                dataType : 'json',
                method : 'POST',
                url : 'new/search/',
                data : {
                    q : encodeURIComponent(request.term),
                    csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val()
                },
                success : function(data) {
                    var users = [];

                    for(var x in data)
                    {
                        users.push({
                            n_c : data[x].fields['n_c'],
                            tipo_p : data[x].fields['tipo_p'],
                            n_p : data[x].fields['n_p']
                        });
                    }

                    cache[request.term] = users;
                    response(users);
                }
            });
        },
        response: function(event, ui) {

            if (ui.content.length === 0) {
                $('.results .error').html('No se encontraron resultados').show();
                $('.results .wrapper').empty();
            }
            else
                $('.results .error').empty().hide();
        }
    }).autocomplete('instance')._renderItem = function(ul, item) {

        var user_tmpl = $('<div />')
                        .addClass('ApellidoyNombres')
                        .append('<a href="/" />').find('a').addClass('ApellidoyNombres').html(item.n_c)
                        .parent()
                        .append('<span class="identity"><strong>Identidad:</strong><span></span></span>')
                        .find('.identity > span').append(item.tipo_p)
                        .parent().parent()
                        .append('<span class="control-label"><strong>nroprontuario:</strong><span></span></span>')
                        .find('.n_p > span').append(item.n_p)
                        .parent().parent();

        return $('<div></div>')
            .data('item.autocomplete', item)
            .append(user_tmpl)
            .appendTo(ul);
    };
}

$(document).ready(__init);
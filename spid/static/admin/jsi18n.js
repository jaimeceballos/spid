
/* gettext library */

var catalog = new Array();

function pluralidx(n) {
  var v=(n != 1);
  if (typeof(v) == 'boolean') {
    return v ? 1 : 0;
  } else {
    return v;
  }
}
catalog['%(sel)s of %(cnt)s selected'] = ['',''];
catalog['%(sel)s of %(cnt)s selected'][0] = '%(sel)s de %(cnt)s seleccionado/a';
catalog['%(sel)s of %(cnt)s selected'][1] = '%(sel)s de %(cnt)s seleccionados/as';
catalog['6 a.m.'] = '6 a.m.';
catalog['Available %s'] = '%s disponibles';
catalog['Calendar'] = 'Calendario';
catalog['Cancel'] = 'Cancelar';
catalog['Choose a time'] = 'Elija una hora';
catalog['Choose all'] = 'Seleccionar todos/as';
catalog['Choose'] = 'Seleccionar';
catalog['Chosen %s'] = '%s seleccionados/as';
catalog['Click to choose all %s at once.'] = 'Haga click para seleccionar todos/as los/as %s.';
catalog['Click to remove all chosen %s at once.'] = 'Haga clic para deselecionar todos/as los/as %s.';
catalog['Clock'] = 'Reloj';
catalog['Filter'] = 'Filtro';
catalog['Hide'] = 'Ocultar';
catalog['January February March April May June July August September October November December'] = 'Enero Febrero Marzo Abril Mayo Junio Julio Agosto Setiembre Octubre Noviembre Diciembre';
catalog['Midnight'] = 'Medianoche';
catalog['Noon'] = 'Mediod\u00eda';
catalog['Now'] = 'Ahora';
catalog['Remove all'] = 'Eliminar todos/as';
catalog['Remove'] = 'Eliminar';
catalog['S M T W T F S'] = 'D L M M J V S';
catalog['Show'] = 'Mostrar';
catalog['This is the list of available %s. You may choose some by selecting them in the box below and then clicking the "Choose" arrow between the two boxes.'] = 'Esta es la lista de %s disponibles. Puede elegir algunos/as seleccion\u00e1ndolos/as en el cuadro de abajo y luego haciendo click en la flecha "Seleccionar" ubicada entre las dos listas.';
catalog['This is the list of chosen %s. You may remove some by selecting them in the box below and then clicking the "Remove" arrow between the two boxes.'] = 'Esta es la lista de %s seleccionados. Puede deseleccionar algunos de ellos activ\u00e1ndolos en la lista de abajo y luego haciendo click en la flecha "Eliminar" ubicada entre las dos listas.';
catalog['Today'] = 'Hoy';
catalog['Tomorrow'] = 'Ma\u00f1ana';
catalog['Type into this box to filter down the list of available %s.'] = 'Escriba en esta caja para filtrar la lista de %s disponibles.';
catalog['Yesterday'] = 'Ayer';
catalog['You have selected an action, and you haven\'t made any changes on individual fields. You\'re probably looking for the Go button rather than the Save button.'] = 'Ha seleccionado una acci\u00f3n pero no ha realizado ninguna modificaci\u00f3n en campos individuales. Es probable que lo que necesite usar en realidad sea el bot\u00f3n Ejecutar y no el bot\u00f3n Guardar.';
catalog['You have selected an action, but you haven\'t saved your changes to individual fields yet. Please click OK to save. You\'ll need to re-run the action.'] = 'Ha seleccionado una acci\u00f3n, pero todav\u00eda no ha grabado las modificaciones que ha realizado en campos individuales. Por favor haga click en Aceptar para grabarlas. Necesitar\u00e1 ejecutar la acci\u00f3n nuevamente.';
catalog['You have unsaved changes on individual editable fields. If you run an action, your unsaved changes will be lost.'] = 'Tiene modificaciones sin guardar en campos modificables individuales. Si ejecuta una acci\u00f3n las mismas se perder\u00e1n.';


function gettext(msgid) {
  var value = catalog[msgid];
  if (typeof(value) == 'undefined') {
    return msgid;
  } else {
    return (typeof(value) == 'string') ? value : value[0];
  }
}

function ngettext(singular, plural, count) {
  value = catalog[singular];
  if (typeof(value) == 'undefined') {
    return (count == 1) ? singular : plural;
  } else {
    return value[pluralidx(count)];
  }
}

function gettext_noop(msgid) { return msgid; }

function pgettext(context, msgid) {
  var value = gettext(context + '\x04' + msgid);
  if (value.indexOf('\x04') != -1) {
    value = msgid;
  }
  return value;
}

function npgettext(context, singular, plural, count) {
  var value = ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
  if (value.indexOf('\x04') != -1) {
    value = ngettext(singular, plural, count);
  }
  return value;
}

function interpolate(fmt, obj, named) {
  if (named) {
    return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
  } else {
    return fmt.replace(/%s/g, function(match){return String(obj.shift())});
  }
}

/* formatting library */

var formats = new Array();

formats['DATETIME_FORMAT'] = 'j N Y H:i:s';
formats['DATE_FORMAT'] = 'j N Y';
formats['DECIMAL_SEPARATOR'] = ',';
formats['MONTH_DAY_FORMAT'] = 'j \\d\\e F';
formats['NUMBER_GROUPING'] = '3';
formats['TIME_FORMAT'] = 'H:i:s';
formats['FIRST_DAY_OF_WEEK'] = '0';
formats['TIME_INPUT_FORMATS'] = ['%H:%M:%S', '%H:%M'];
formats['THOUSAND_SEPARATOR'] = '.';
formats['DATE_INPUT_FORMATS'] = ['%d/%m/%Y', '%d/%m/%y', '%Y-%m-%d'];
formats['YEAR_MONTH_FORMAT'] = 'F Y';
formats['SHORT_DATE_FORMAT'] = 'd/m/Y';
formats['SHORT_DATETIME_FORMAT'] = 'd/m/Y H:i';
formats['DATETIME_INPUT_FORMATS'] = ['%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M', '%d/%m/%y %H:%M:%S', '%d/%m/%y %H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M', '%Y-%m-%d'];

function get_format(format_type) {
    var value = formats[format_type];
    if (typeof(value) == 'undefined') {
      return format_type;
    } else {
      return value;
    }
}

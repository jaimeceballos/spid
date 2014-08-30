function initMenu() {

  $('#menu ul').hide();
   //   $('#menu li ul').hide();
  //$('#menu ul:first').show();
  $('#menu li a').click(
    function() {
      var checkElement = $(this).next();
      if((checkElement.is('ul')) && (checkElement.is(':visible'))) {
      $('#menu ul').hide();
        return false;
        }
      if((checkElement.is('ul')) && (!checkElement.is(':visible'))) {
         checkElement.slideDown('normal');
      //   $('#menu li ul').hide();
        return false;
        }
      }
       
     );
  }
$(document).ready(function() {initMenu();});

(function($) {
	$.fn.scrollablecombo = function(options) {
		var opts = $.extend({}, $.fn.scrollablecombo.defaults, options);
		return this.each(function() {
			$this = $(this);
			var o = $.meta ? $.extend({}, opts, $this.data()) : opts;
			
			function findHighestZIndex(){
				var divs = document.getElementsByTagName('div');
				var highest = 0;
				for (var i = 0; i < divs .length; i++)
				{
					var zindex = divs[i].style.zIndex;
					if (zindex > highest) {
						highest = zindex;
					}
				}
				return highest;
			}

			/** 
			* hide the select element
			* graceful degradation
			*/
			$this.hide();
			
			function makeScrollable($wrapper, $container){
				var extra 			= 50;
				var wrapperHeight 	= $wrapper.height() ;
				$wrapper.css({overflow: 'auto'});
				$wrapper.scrollTop(0);
				$wrapper.unbind('mousemove').bind('mousemove',function(e){
					var ulHeight 	= $container.outerHeight() + 2*extra ;
					var top 		= (e.pageY - $wrapper.offset().top) * (ulHeight-wrapperHeight ) / wrapperHeight - extra;
					$wrapper.scrollTop(top);
				});
			}
			
			/**
			* let's build our element structure
			*/
			var $ul_e 	= $('<ul />');
			
			$this.find('option').each(function(){
				var $option = $(this);
				var liclass = '';
				if($option.attr('selected'))
					liclass = 'selected';
				var $li_e 	= $('<li />',{
					className	:	liclass,
					html		:	'<a href="'+$option.val()+'">'+$option.html()+'</a>'
				});
				$ul_e.append($li_e);
			});
			
			var $wrapper_e 	= $('<div />',{
				className	:	'cb_selectWrapper'
			});
			
			$wrapper_e.append($ul_e);
			
			var $control_e 	= $('<div />',{
				//id			:	'ui_element',
				className	:	'cb_selectMain cb_down'
			});
			
			var $select_e 	= $('<div />',{
				className	:	'cb_select'
			});
			
			$select_e.append($wrapper_e).append($control_e);
			
			var $selected	= $ul_e.find('.selected');
			
			
			function openCombo(){
				var maxzidx = Math.max(findHighestZIndex(),99999);
				$wrapper_e.css('z-index',parseInt(maxzidx+1000)).show();
				$control_e.addClass('cb_up').removeClass('cb_down');
				makeScrollable($wrapper_e,$ul_e);
			}
			function closeCombo(){
				$wrapper_e.css('z-index',1000).hide();
				$control_e.addClass('cb_down').removeClass('cb_up');
			}
			$control_e.html($selected.find('a').html())
					  .bind('click',function(){
						  (!$wrapper_e.is(':visible'))? openCombo() : closeCombo();
					  }
			);
			$selected.hide();
			
			$this.parent().append($select_e);
			$this.remove();
			
			$ul_e.find('a').bind('click',function(e){
				var $this 		= $(this);
				$control_e.html($this.html());
				var $selected	= $ul_e.find('.selected');
				$selected.show().removeClass('selected');
				$this.parent().addClass('selected').hide();
				closeCombo();
				e.preventDefault();
			});
			
			
			
		});
	};
	$.fn.scrollablecombo.defaults = {
		
	};
})(jQuery);

(function($) {
        /* private variable "oHover" used to determine if you're still hovering over the same element */
        var textarea, staticOffset;  // added the var declaration for 'staticOffset' thanks to issue logged by dec.
        var iLastMousePos = 0;
        var iMin = 32;
        var grip;
        /* TextAreaResizer plugin */
        $.fn.TextAreaResizer = function() {
                return this.each(function() {
                    textarea = $(this).addClass('processed'), staticOffset = null;

                        // 18-01-08 jQuery bind to pass data element rather than direct mousedown - Ryan O'Dell
                    // When wrapping the text area, work around an IE margin bug.  See:
                    // http://jaspan.com/ie-inherited-margin-bug-form-elements-and-haslayout
                    $(this).wrap('<div class="resizable-textarea"><span></span></div>')
                      .parent().append($('<div class="grippie"></div>').bind("mousedown",{el: this} , startDrag));

                    var grippie = $('div.grippie', $(this).parent())[0];
                    grippie.style.marginRight = (grippie.offsetWidth - $(this)[0].offsetWidth) +'px';

                });
        };
        /* private functions */
        function startDrag(e) {
                textarea = $(e.data.el);
                textarea.blur();
                iLastMousePos = mousePosition(e).y;
                staticOffset = textarea.height() - iLastMousePos;
                textarea.css('opacity', 0.25);
                $(document).mousemove(performDrag).mouseup(endDrag);
                return false;
        }

        function performDrag(e) {
                var iThisMousePos = mousePosition(e).y;
                var iMousePos = staticOffset + iThisMousePos;
                if (iLastMousePos >= (iThisMousePos)) {
                        iMousePos -= 5;
                }
                iLastMousePos = iThisMousePos;
                iMousePos = Math.max(iMin, iMousePos);
                textarea.height(iMousePos + 'px');
                if (iMousePos < iMin) {
                        endDrag(e);
                }
                return false;
        }

        function endDrag(e) {
                $(document).unbind('mousemove', performDrag).unbind('mouseup', endDrag);
                textarea.css('opacity', 1);
                textarea.focus();
                textarea = null;
                staticOffset = null;
                iLastMousePos = 0;
        }

        function mousePosition(e) {
                return { x: e.clientX + document.documentElement.scrollLeft, y: e.clientY + document.documentElement.scrollTop };
        };
})(jQuery);

//-------------------- vanadium-jquery.js -----------------------------


Vanadium = {};
Vanadium.Version = '0.1';
Vanadium.CompatibleWithJQuery = '1.3.2';
Vanadium.Type = "jquery";

if (jQuery().jquery.indexOf(Vanadium.CompatibleWithJQuery) != 0 && window.console && window.console.warn)
  console.warn("This version of Vanadium is tested with jQuery " + Vanadium.CompatibleWithJQuery +
               " it may not work as expected with this version (" + jQuery().jquery + ")");

Vanadium.each = jQuery.each;

Vanadium.all_elements = function() {
  return jQuery('*');
};

Vanadium.partition = function(elements, dyscriminator) {
  var left = [];
  var right = [];
  Vanadium.each(elements, function() {
    if (dyscriminator(this)) {
      left.push(this);
    } else {
      right.push(this);
    }
    ;
  });
  return [left, right];
};




//-------------------- vanadium-hashmap.js -----------------------------


var HashMap = function() {
  this.initialize();
}

HashMap.hashmap_instance_id = 0;

HashMap.prototype = {
  hashkey_prefix: "<#HashMapHashkeyPerfix>",
  hashcode_field: "<#HashMapHashcodeField>",

  initialize: function() {
    this.backing_hash = {};
    this.code = 0;
    HashMap.hashmap_instance_id += 1;
    this.instance_id = HashMap.hashmap_instance_id;
  },

  hashcodeField: function() {
    return this.hashcode_field + this.instance_id;
  },
  /*
   maps value to key returning previous assocciation
   */
  put: function(key, value) {
    var prev;

    if (key && value) {
      var hashCode;
      if (typeof(key) === "number" || typeof(key) === "string") {
        hashCode = key;
      } else {
        hashCode = key[this.hashcodeField()];
      }
      if (hashCode) {
        prev = this.backing_hash[hashCode];
      } else {
        this.code += 1;
        hashCode = this.hashkey_prefix + this.code;
        key[this.hashcodeField()] = hashCode;
      }
      this.backing_hash[hashCode] = [key, value];
    }
    return prev === undefined ? undefined : prev[1];
  },
  /*
   returns value associated with given key
   */
  get: function(key) {
    var value;
    if (key) {
      var hashCode;
      if (typeof(key) === "number" || typeof(key) === "string") {
        hashCode = key;
      } else {
        hashCode = key[this.hashcodeField()];
      }
      if (hashCode) {
        value = this.backing_hash[hashCode];
      }
    }
    return value === undefined ? undefined : value[1];
  },
  /*
   deletes association by given key.
   Returns true if the assocciation existed, false otherwise
   */
  del: function(key) {
    var success = false;
    if (key) {
      var hashCode;
      if (typeof(key) === "number" || typeof(key) === "string") {
        hashCode = key;
      } else {
        hashCode = key[this.hashcodeField()];
      }
      if (hashCode) {
        var prev = this.backing_hash[hashCode];
        this.backing_hash[hashCode] = undefined;
        if (prev !== undefined){
          key[this.hashcodeField()] = undefined; //let's clean the key object
          success = true;
        }
      }
    }
    return success;
  },
  /*
   iterate over key-value pairs passing them to provided callback
   the iteration process is interrupted when the callback returns false.
   the execution context of the callback is the value of the key-value pair
   @ returns the HashMap (so we can chain)                                                                  (
   */
  each: function(callback, args) {
    var key;
    for (key in this.backing_hash){
      if (callback.call(this.backing_hash[key][1], this.backing_hash[key][0], this.backing_hash[key][1]) === false)
        break;
    }
    return this;
  },
  toString: function() {
    return "HashMapJS"
  }

}


//-------------------- vanadium-container.js -----------------------------


Vanadium.containers = new HashMap();

var ContainerValidation = function(html_element) {
  this.initialize(html_element)
}

ContainerValidation.prototype = {
  initialize: function(html_element) {
    this.html_element = html_element;
    this.elements = [];
  },
  add_element: function(element) {
    this.elements.push(element);
  },
  decorate: function() {
    var valid = null;
    for (var id in this.elements) {
      if (this.elements[id].invalid === undefined) {
        valid = undefined;
      } else if (this.elements[id].invalid === true) {
        valid = false;
        break;
      } else if (this.elements[id].invalid === false && valid === null) {
        valid = true;
      }
    }
    if (valid === undefined) {
      jQuery(this.html_element).removeClass(Vanadium.config.invalid_class);
      jQuery(this.html_element).removeClass(Vanadium.config.valid_class);
    } else if (valid) {
      jQuery(this.html_element).removeClass(Vanadium.config.invalid_class);
      jQuery(this.html_element).addClass(Vanadium.config.valid_class);
    } else {
      jQuery(this.html_element).removeClass(Vanadium.config.valid_class);
      jQuery(this.html_element).addClass(Vanadium.config.invalid_class);
    }
  }
}

//-------------------- vanadium-form.js -----------------------------
var VanadiumForm = function(element) {
    this.initialize(element);
}

Vanadium.forms = new HashMap();

VanadiumForm.add_element = function(validation_element) {
    var form = validation_element.element.form;
    if (form) {
        var vanadum_form = Vanadium.forms.get(form);
        if (vanadum_form) {
            vanadum_form.validation_elements.push(validation_element);
        } else {
            vanadum_form = new VanadiumForm(validation_element);
            Vanadium.forms.put(form, vanadum_form);
        }
    }
}
VanadiumForm.prototype = {

    initialize: function(validation_element) {
        this.validation_elements = [validation_element];
        this.form = validation_element.element.form;
        var self = this;
        var on_form_submit = function() {
            var validation_result = self.validate();

            var success = true;
            validation_result.each(function(_element, validation_results) {
                for (var r in validation_results) {
                    if (validation_results[r].success == false) {
                        success = false;
                        break;
                    }
                }
                if (success == false) {
                    return false;// break from hashmap iteration
                }
            });
            if (!success) {
                self.decorate();
                return false;
            }
            return success;
        };

        //jQuery(this.form).submit(on_form_submit);
        jQuery(this.form).find(':submit').click(function() {
            return on_form_submit();
        });

        this.form.decorate = function() {
            self.decorate();
        }
    },

    validate: function() {
        var validation = new HashMap();
        Vanadium.each(this.validation_elements,
                function() {
                    validation.put(this, this.validate());
                });
        return validation;
    },

    decorate: function(validation_results) {
        if (arguments.length == 0) {
            validation_results = this.validate();
        }
        validation_results.each(function(element, element_validation_results) {
            element.decorate(element_validation_results);
        });
    },

    validateAndDecorate: function() {
        this.decorate(this.validate())
    }
}
//-------------------- vanadium-base.js -----------------------------
Vanadium.validators_types = {};
Vanadium.elements_validators_by_id = {};
Vanadium.all_elements_validators = [];
Vanadium.created_advices = [];

Vanadium.all_html_elements = new HashMap();


//default config
Vanadium.config = {
    valid_class: 'vanadium-valid',
    invalid_class: 'vanadium-invalid',
    message_value_class: 'vanadium-message-value',
    advice_class: 'vanadium-advice',
    prefix: ':',
    separator: ';',
    reset_defer_timeout: 100
}

Vanadium.empty_advice_marker_class = '-vanadium-empty-advice-'

//validation rules
Vanadium.rules = {}


Vanadium.init = function() {
    this.setupValidatorTypes();
    this.scan_dom();
}


Vanadium.addValidatorType = function(className, validationFunction, error_message, message, init) {
    this.validators_types[className] = new Vanadium.Type(className, validationFunction, error_message, message, init);
};

Vanadium.addValidatorTypes = function(validators_args) {
    var self = this;
    Vanadium.each(validators_args,
            function() {
                Vanadium.addValidatorType.apply(self, this);
            }
            )
};


Vanadium.scan_dom = function() {
    Vanadium.each(Vanadium.all_elements(),
            function(_idx, child) {

                var class_names = child.className.split(' ');
                if (Vanadium.is_input_element(child)) {
                    var element_validation = new ElementValidation(child);

                    if (child.id)
                        Vanadium.elements_validators_by_id[child.id] = element_validation

                    Vanadium.all_elements_validators.push(element_validation)
                    Vanadium.all_html_elements.put(child, element_validation);

                    VanadiumForm.add_element(element_validation);

                    //create validation rules based on class markup
                    Vanadium.each(class_names,
                            function() {
                                var parameters = Vanadium.parse_class_name(this);
                                /*'this' is class_name*/
                                if (parameters) {
                                    Vanadium.add_validation_instance(element_validation, parameters);
                                    Vanadium.add_validation_modifier(element_validation, parameters);
                                }
                            });
                    //create validation rules based on json providen in VanadiumRules variable
                    Vanadium.each(Vanadium.get_rules(child.id),
                            function() {
                                var parameters = this;
                                if (parameters) {
                                    Vanadium.add_validation_instance(element_validation, parameters);
                                    Vanadium.add_validation_modifier(element_validation, parameters);
                                }
                            });
                    element_validation.setup();
                } else {
                    Vanadium.add_validation_container(child);
                }
            })
}

Vanadium.add_validation_container = function(element) {
    var class_names = element.className.split(' ');
    Vanadium.each(class_names,
            function() {
                var parameters = Vanadium.parse_class_name(this);
                if (parameters[0] == 'container') {
                    Vanadium.containers.put(element, new ContainerValidation(element));
                    return true
                }
            });
    Vanadium.each(Vanadium.get_rules(element.id),
            function() {
                var rule = this;
                if (rule == 'container') {
                    Vanadium.containers.put(element, new ContainerValidation(element));
                    return true
                }
            });
}

Vanadium.get_rules = function(element_id) {
    var rule_from_string_or_hash = function(r) {
        if (typeof r === "string") {
            return [r];
        } else if (Vanadium.isArray(r)) {
            return r;
        } else if (typeof(r) === "object") {
            return [r.validator, r.parameter, r.advice];
        } else {
            return undefined;
        }
    }
    //
    var rules = [];
    //
    var rs = Vanadium.rules[element_id];
    if (typeof rs === "undefined") {
        return [];
    } else if (typeof rs === "string") {
        rules.push(rs);
    } else if (Vanadium.isArray(rs)) {
        for (var r in rs) {
            rules.push(rule_from_string_or_hash(rs[r]));
        }
    } else if (typeof(rs) === "object") {
        rules.push(rule_from_string_or_hash(rs));
    }
    return rules;
}

Vanadium.parse_class_name = function(class_name) {
    if (class_name.indexOf(Vanadium.config.prefix) == 0) {
        var v_params = class_name.substr(Vanadium.config.prefix.length).split(Vanadium.config.separator)
        for (var key in v_params) {
            if (v_params[key] == "") {
                v_params[key] = undefined
            }
        }
        return v_params;
    } else {
        return [];
    }
}

Vanadium.add_validation_instance = function(element_validation, parameters) {
    var v_name = parameters[0];
    var v_param = parameters[1];
    var v_advice_id = parameters[2];
    var validator_type = Vanadium.validators_types[v_name]
    if (validator_type) {
        element_validation.add_validation_instance(validator_type, v_param, v_advice_id);
    }
}

Vanadium.add_validation_modifier = function(element_validation, parameters) {
    var m_name = parameters[0];
    var m_param = parameters[1];
    if (m_name == 'only_on_blur' || m_name == 'only_on_submit' || m_name == 'wait' || m_name == 'advice') {
        element_validation.add_validation_modifier(m_name, m_param);
    }
}

Vanadium.validate = function() {
    var validation = new HashMap();
    Vanadium.each(Vanadium.all_elements_validators,
            function() {
                validation.put(this, this.validate());
            });
    return validation;
}

Vanadium.validateAndDecorate = function(html_element) {
    if (typeof html_element === "undefined") {  // validate and decorate everything
        Vanadium.decorate(Vanadium.validate());
    } else if (html_element.nodeType == 1) {
        var element_validation = Vanadium.all_html_elements.get(html_element) || Vanadium.forms.get(html_element);
        if (element_validation) {
            element_validation.validateAndDecorate(false);
        }
    }
}

Vanadium.decorate = function(validation_results) {
    if (typeof validation_results === "object") {
        if (validation_results.toString() == "HashMapJS") {
            validation_results.each(function(element, element_validation_results) {
                element.decorate(element_validation_results);
            })
        } else {//this is probably json structure representing validation result
            var element_id;
            for (element_id in validation_results) {
                var element = Vanadium.elements_validators_by_id[element_id];
                if (element) {
                    element.decorate(validation_results[element_id]);
                }
            }
        }
    }
}

Vanadium.reset = function() {
    Vanadium.each(Vanadium.all_elements_validators,
            function() {
                this.reset();
            });
}

//-------------------- vanadium-utils.js -----------------------------

Vanadium.isArray = function(object) {
  return object != null && typeof object == "object" &&
         'splice' in object && 'join' in object;

}

Vanadium.isFunction = function(object) {
  return object != null && object.toString() === "[object Function]";
}

Vanadium.extend = function(extension) {
  var args = [Vanadium];
  for (var idx = 0; idx < arguments.length; idx++) {
    args.push(arguments[idx]);
  }
  return jQuery.extend.apply(jQuery, args);
}

Vanadium.bind = function(fun, context) {
  return function() {
    return fun.apply(context, arguments);
  }
}

//-------------------- vanadium-dom.js -----------------------------
Vanadium.extend(
{

  /**
   *	gets the type of element, to check whether it is compatible
   */
  getElementType: function(element) {
    switch (true) {
      case (element.nodeName.toUpperCase() == 'TEXTAREA'):
        return Vanadium.TEXTAREA;
      case (element.nodeName.toUpperCase() == 'INPUT' && element.type.toUpperCase() == 'TEXT'):
        return Vanadium.TEXT;
      case (element.nodeName.toUpperCase() == 'INPUT' && element.type.toUpperCase() == 'PASSWORD'):
        return Vanadium.PASSWORD;
      case (element.nodeName.toUpperCase() == 'INPUT' && element.type.toUpperCase() == 'CHECKBOX'):
        return Vanadium.CHECKBOX;
      case (element.nodeName.toUpperCase() == 'INPUT' && element.type.toUpperCase() == 'FILE'):
        return Vanadium.FILE;
      case (element.nodeName.toUpperCase() == 'SELECT' && element.type.toUpperCase() == 'OPTION'):
        return Vanadium.SELECT;
      case (element.nodeName.toUpperCase() == 'INPUT'):
        throw new Error('Vanadium::getElementType - Cannot use Vanadium on an ' + element.type + ' input!');
      default:
        throw new Error('Vanadium::getElementType - Element must be an input, select, or textarea!');
    }
    ;
  },
  is_input_element : function(element) {
    return (element.nodeName.toUpperCase() == 'TEXTAREA') ||
           (element.nodeName.toUpperCase() == 'INPUT' && element.type.toUpperCase() == 'TEXT') ||
           (element.nodeName.toUpperCase() == 'INPUT' && element.type.toUpperCase() == 'PASSWORD') ||
           (element.nodeName.toUpperCase() == 'INPUT' && element.type.toUpperCase() == 'CHECKBOX') ||
           (element.nodeName.toUpperCase() == 'INPUT' && element.type.toUpperCase() == 'FILE') ||
           (element.nodeName.toUpperCase() == 'SELECT' && element.type.toUpperCase() == 'OPTION')
  },
  /**
   *	makes a span containg the passed or failed advice
   *
   * @return {HTMLSpanObject} - a span element with the advice message in it
   */
  createAdvice: function(element, advice_id, message) {
    var advice = document.createElement('span');
    advice.id = advice_id;
    var textNode = document.createTextNode(message);
    advice.appendChild(textNode);
    element.parentNode.insertBefore(advice, element.nextSibling);
    this.created_advices.push(advice);
  },

  /**
   *	adds the class of the element/advice/container to indicte if valid or not
   */
  addValidationClass: function(element, valid) {
    if (element) {
      this.removeValidationClass(element);
      if (valid) {
        element.className += ' ' + Vanadium.config.valid_class;
      } else {
        element.className += ' ' + Vanadium.config.invalid_class;
      }
      ;
    }
    ;
  },
  /**
   *	removes the class that has been applied to the element/advice/container to indicte if valid or not
   */
  removeValidationClass: function(element) {
    if (element) {
      if (element.className.indexOf(Vanadium.config.invalid_class) != -1) element.className = element.className.split(Vanadium.config.invalid_class).join(' ');
      if (element.className.indexOf(Vanadium.config.valid_class) != -1) element.className = element.className.split(Vanadium.config.valid_class).join(' ');
    }
    ;
  },
  /** element types constants ****/
  TEXTAREA: 1,
  TEXT: 2,
  PASSWORD: 3,
  CHECKBOX: 4,
  SELECT: 5,
  FILE: 6
}
        );


//-------------------- vanadium-element.js -----------------------------


ElementValidation = function(element) {
  this.initialize(element)
};
ElementValidation.prototype = {

  initialize: function(element) {
    this.virgin = true;
    this.element = element;
    this.validations = [];
    this.only_on_blur = false;
    this.only_on_submit = false;
    this.wait = 100;
    this.created_advices = [];
    this.decorated = false;
    this.containers = null;
    this.invalid = undefined;
    this.advice_id = undefined; //this is general common advice for all validation instances having no specific advice defined
  },

  add_validation_instance: function(validator_type, param, advice_id) {
    this.validations.push(new Validation(this.element, validator_type, param, advice_id));
  },
  add_validation_modifier: function(modifier, param) {
    if (modifier == 'only_on_blur') {
      //  whether you want it to validate as you type or only on blur  (DEFAULT: false)
      this.only_on_blur = true
    } else if (modifier == 'only_on_submit') {
      //  whether should be validated only when the form it belongs to is submitted (DEFAULT: false)
      this.only_on_submit = true
    } else if (modifier == 'wait') {
      //  the time you want it to pause from the last keystroke before it validates (ms) (DEFAULT: 0)
      var milisesonds = parseInt(param);
      if (milisesonds != NaN && typeof(milisesonds) === "number") {
        this.wait = milisesonds;
      }
      ;
    } else if (modifier == 'advice') {
      var advice = document.getElementById(param);
      if (advice) {
        this.advice_id = param;
      }
    }
    ;
  },
  element_containers: function() {
    if (this.containers === null) {
      this.containers = new HashMap();
      var parent = this.element.parentNode;
      //search up the DOM tree
      while (parent != document) {
        var container = Vanadium.containers.get(parent);
        if (container) {
          container.add_element(this);
          this.containers.put(parent, container);
        }
        ;
        parent = parent.parentNode;
      }
      ;
    }
    ;
    return this.containers;
  },
  // context - the contect in which decoration_callback should be invoked
  // decoration_callback - the decoration used by asynchronous validation
  validate: function(decoration_context, decoration_callback) {
    var result = [];
    Vanadium.each(this.validations, function() {
      result.push(this.validate(decoration_context, decoration_callback));
    });
    return result;
  },
  decorate: function(element_validation_results, do_not_reset) {
    if (!do_not_reset) {
      this.reset();
    }
    this.decorated = true;
    var self = this;
    var passed_and_failed = Vanadium.partition(element_validation_results, function(validation_result) {
      return validation_result.success
    });
    var passed = passed_and_failed[0];
    var failed = passed_and_failed[1];
    // add apropirate CSS class to the validated element
    if (failed.length > 0) {
      this.invalid = true; //mark this validation element as invalid
      Vanadium.addValidationClass(this.element, false);
    } else if (passed.length > 0 && !this.invalid) { //when valid result comes but the previous was invalid and no reset was done, the invalid flag should stay unchanged
      this.invalid = false; //mark this validation element as valid
      Vanadium.addValidationClass(this.element, true);
    } else {
      this.invalid = undefined; //mark this validation element as undefined
    }
    ;
    // add apropirate CSS class to the validated element's containers
    this.element_containers().each(function(_element, container) {
      container.decorate();
    });
    //
    Vanadium.each(failed, function(_idx, validation_result) {
      var advice = undefined;
      if (self.advice_id) {
        advice = document.getElementById(self.advice_id);
      }
      if (advice || validation_result.advice_id) {
        advice = advice || document.getElementById(validation_result.advice_id);
        if (advice) {
          jQuery(advice).addClass(Vanadium.config.advice_class);
          var advice_is_empty = advice.childNodes.length == 0
          if (advice_is_empty || jQuery(advice).hasClass(Vanadium.empty_advice_marker_class)) {
            jQuery(advice).addClass(Vanadium.empty_advice_marker_class);
            jQuery(advice).append("<span>" + validation_result.message + "</span>");
          }
          ;
          jQuery(advice).show();
        } else {
          advice = self.create_advice(validation_result);
        }
        ;
      } else {
        advice = self.create_advice(validation_result);
      }
      ;
      Vanadium.addValidationClass(advice, false);
    });
  },
  validateAndDecorate : function(regard_virginity) {
    //That's tricky one ;)
    // 1. we are runing validate to get all validation results
    // 2. there could be possible some validations running asynchronous
    // so we won't get the result imediately. In that case the provided decoration callback
    // will be invoked on return from asynchronous callback
    // It is used by Ajax based server-side validation
    if(!regard_virginity || !this.virgin)
      this.decorate(this.validate(this, this.decorate));
  },
  create_advice: function(validation_result) {
    var span = document.createElement("span");
    this.created_advices.push(span);
    jQuery(span).addClass(Vanadium.config.advice_class);
    jQuery(span).html(validation_result.message);
    jQuery(this.element).after(span);
    return span;
  },
  reset: function() {
    this.invalid = undefined; //mark this validation element as undefined
    //    this.element_containers().each(function(_element, container) {
    //      container.decorate();
    //    });
    var element_advice = document.getElementById(this.advice_id);
    if (element_advice) {
      if (jQuery(element_advice).hasClass(Vanadium.empty_advice_marker_class)) {
        jQuery(element_advice).empty();
      }
      jQuery(element_advice).hide();
    }
    Vanadium.each(this.validations, function() {
      var advice = document.getElementById(this.adviceId);
      if (advice) {
        if (jQuery(advice).hasClass(Vanadium.empty_advice_marker_class)) {
          jQuery(advice).empty();
        }
        jQuery(advice).hide();
      }
      ;
    });

    var created_advice = this.created_advices.pop();
    while (!(created_advice === undefined)) {
      jQuery(created_advice).remove();
      created_advice = this.created_advices.pop();
    }
    ;
    Vanadium.removeValidationClass(this.element);
  },
  //
  //
  //
  /**
   * makes the validation wait the alotted time from the last keystroke
   */
  deferValidation: function() {
    if (this.wait >= 300) this.reset();
    var self = this;
    if (self.timeout) clearTimeout(self.timeout);
    self.timeout = setTimeout(function() {
      jQuery(self.element).trigger('validate');
    }, self.wait);
  },
  deferReset: function() {
    var self = this;
    if (self.reset_timeout) clearTimeout(self.reset_timeout);
    self.reset_timeout = setTimeout(function() {
      self.reset();
    }, Vanadium.config.reset_defer_timeout);
  },
  setup: function() {
    var self = this;
    this.elementType = Vanadium.getElementType(this.element);

    this.form = this.element.form;

    this.element_containers();

    if (!this.only_on_submit) {
      this.observe();
      jQuery(self.element).bind('validate', function() {
        self.validateAndDecorate.call(self, true)
      });
      jQuery(self.element).bind('defer_validation', function() {
        self.deferValidation.call(self)
      });
      jQuery(self.element).bind('reset', function() {
        self.reset.call(self)
      });
    }

  },
  observe: function() {
    var element = this.element;
    var elementType = Vanadium.getElementType(element);
    var self = this;
    jQuery(element).focus(function() {
      self.virgin = false;
    });
    switch (elementType) {
      case Vanadium.CHECKBOX:
        jQuery(element).click(function() {
          //TODO check db click !!!
          self.virgin = false; //this is here 'cos safari do not focus on checkboxes
          jQuery(self.element).trigger('validate');
        });
        break;
      //TODO check if checkboxes support on-change too. and if yes handle it!
      // let it run into the next to add a change event too
      case Vanadium.SELECT:
          jQuery(element).change(function() {
          jQuery(self.element).trigger('validate');
          });
      case Vanadium.FILE:
        jQuery(element).change(function() {
          jQuery(element).trigger('validate');
        });
        break;
      default:
        jQuery(element).keydown(function(e) {
          if (e.keyCode != 9) {//no tabulation as it changes focus
            jQuery(element).trigger('reset');
          }
          ;
        });

        if (!this.only_on_blur) {
          jQuery(element).keyup(function(e) {
            if (e.keyCode != 9) {//no tabulation as it changes focus
              jQuery(element).trigger('defer_validation');
            }
            ;
          });
        };
        jQuery(element).blur(function() {
          jQuery(element).trigger('validate');
        });
    }
  }
};

//-------------------- vanadium-instance.js -----------------------------


var Validation = function(element, validation_type, param, advice_id) {
  this.initialize(element, validation_type, param, advice_id)
}

Validation.prototype = {
  initialize: function(element, validation_type, param, advice_id) {
    this.element = element;
    this.validation_type = validation_type;
    this.param = param;
    //
    this.adviceId = advice_id;
    var advice = document.getElementById(advice_id);
    if (advice) {
      jQuery(advice).addClass(Vanadium.config.advice_class);
    }
    if(this.validation_type.init){//Vanadium.isFunction(this.validation_type.init)){
      this.validation_type.init(this); //this give us oportunity to define in validation_type scope activity which will be performed on its instance initialisation
    }
  },
  emmit_message: function(message) {
    if (typeof(message) === "string") {
      return message;
    } else if (typeof(message) === "function") {
      return message.call(this, jQuery(this.element).val(), this.param);
    }
  },
  validMessage: function() {
    return this.emmit_message(this.validation_type.validMessage()) || 'ok'
  },
  invalidMessage: function() {
    return this.emmit_message(this.validation_type.invalidMessage()) || 'error'
  },
  test: function(decoration_context, decoration_callback) {
    return this.validation_type.validationFunction.call(this, jQuery(this.element).val(), this.param, this, decoration_context, decoration_callback);
  },
  // decoration_context - the contect in which decoration_callback should be invoked
  // decoration_callback - the decoration used by asynchronous validation
  validate: function(decoration_context, decoration_callback) {
    var return_value = {
      success: false,
      message: "Received invalid return value."
    }
    var validation_result = this.test(decoration_context, decoration_callback);
    if (typeof validation_result === "boolean") {
      return {
        success: validation_result,
        advice_id: this.adviceId,
        message: (validation_result ? this.validMessage() : this.invalidMessage())
      }
    } else if (typeof validation_result === "object") {
      jQuery.extend.apply(return_value, validation_result);
    }
    return return_value;
  }
}

//-------------------- vanadium-types.js -----------------------------


Vanadium.Type = function(className, validationFunction, error_message, message, init) {
  this.initialize(className, validationFunction, error_message, message, init);
};
Vanadium.Type.prototype = {
  initialize: function(className, validationFunction, error_message, message, init) {
    this.className = className;
    this.message = message;
    this.error_message = error_message;
    this.validationFunction = validationFunction;
    this.init = init;
  },
  test: function(value) {
    return this.validationFunction.call(this, value);
  },
  validMessage: function() {
    return this.message;
  },
  invalidMessage: function() {
    return this.error_message;
  },
  toString: function() {
    return "className:" + this.className + " message:" + this.message + " error_message:" + this.error_message
  },
  init: function(parameter) {
    if (this.init) {
      this.init(parameter);
    }
  }
};

Vanadium.setupValidatorTypes = function() {

  Vanadium.addValidatorType('empty', function(v) {
    return  ((v == null) || (v.length == 0));
  });

  Vanadium.addValidatorTypes([
    ['equal', function(v, p) {
      return v == p;
    }, function (_v, p) {
      return 'The value should be equal to <span class="' + Vanadium.config.message_value_class + '">' + p + '</span>.'
    }],
    //
    ['equal_ignore_case', function(v, p) {
      return v.toLowerCase() == p.toLowerCase();
    }, function (_v, p) {
      return 'The value should be equal to <span class="' + Vanadium.config.message_value_class + '">' + p + '</span>.'
    }],
    //
    ['required', function(v) {
      return !Vanadium.validators_types['empty'].test(v);
    }, 'datos invalidos'],
    //
    ['accept', function(v, _p, e) {
      return e.element.checked;
    }, 'Must be accepted!'],
    //
    ['integer', function(v) {
      if (Vanadium.validators_types['empty'].test(v)) return true;
      var f = parseFloat(v);
      return (!isNaN(f) && f.toString() == v && Math.round(f) == f);
    }, 'Please enter a valid integer in this field.'],
    //
    ['number', function(v) {
      return Vanadium.validators_types['empty'].test(v) || (!isNaN(v) && !/^\s+$/.test(v));
    }, 'Please enter a valid number in this field.'],
    //
    ['float', function(v) {
      return Vanadium.validators_types['empty'].test(v) || (!isNaN(v) && !/^\s+$/.test(v));
    }, 'Please enter a valid number in this field.'],
    //
    ['digits', function(v) {
      return Vanadium.validators_types['empty'].test(v) || !/[^\d]/.test(v);
    }, 'Please use numbers only in this field. please avoid spaces or other characters such as dots or commas.'],
    //
    ['alpha', function (v) {
      return Vanadium.validators_types['empty'].test(v) || /^[a-zA-Z\u00C0-\u00FF\u0100-\u017E\u0391-\u03D6]+$/.test(v)   //% C0 - FF (Ë - Ø); 100 - 17E (? - ?); 391 - 3D6 (? - ?)
    }, 'Please use letters only in this field.'],
    //
    ['asciialpha', function (v) {
      return Vanadium.validators_types['empty'].test(v) || /^[a-zA-Z]+$/.test(v)   //% C0 - FF (Ë - Ø); 100 - 17E (? - ?); 391 - 3D6 (? - ?)
    }, 'Please use ASCII letters only (a-z) in this field.'],
    ['alphanum', function(v) {
      return Vanadium.validators_types['empty'].test(v) || !/\W/.test(v)
    }, 'Please use only letters (a-z) or numbers (0-9) only in this field. No spaces or other characters are allowed.'],
    //
    ['date', function(v) {
      var test = new Date(v);
      return Vanadium.validators_types['empty'].test(v) || !isNaN(test);
    }, 'Please enter a valid date.'],
    //
    ['email', function (v) {
      return (Vanadium.validators_types['empty'].test(v)
              ||
              /\w{1,}[@][\w\-]{1,}([.]([\w\-]{1,})){1,3}$/.test(v))
    }, 'Please enter a valid email address. For example fred@domain.com .'],
    //
    ['url', function (v) {
      return Vanadium.validators_types['empty'].test(v) || /^(http|https|ftp):\/\/(([A-Z0-9][A-Z0-9_-]*)(\.[A-Z0-9][A-Z0-9_-]*)+)(:(\d+))?\/?/i.test(v)
    }, 'Please enter a valid URL.'],
    //
    ['date_au', function(v) {
      if (Vanadium.validators_types['empty'].test(v)) return true;
      var regex = /^(\d{2})\/(\d{2})\/(\d{4})$/;
      if (!regex.test(v)) return false;
      var d = new Date(v.replace(regex, '$2/$1/$3'));
      return ( parseInt(RegExp.$2, 10) == (1 + d.getMonth()) ) && (parseInt(RegExp.$1, 10) == d.getDate()) && (parseInt(RegExp.$3, 10) == d.getFullYear() );
    }, 'Please use this date format: dd/mm/yyyy. For example 17/03/2006 for the 17th of March, 2006.'],
    //
    ['currency_dollar', function(v) {
      // [$]1[##][,###]+[.##]
      // [$]1###+[.##]
      // [$]0.##
      // [$].##
      return Vanadium.validators_types['empty'].test(v) || /^\$?\-?([1-9]{1}[0-9]{0,2}(\,[0-9]{3})*(\.[0-9]{0,2})?|[1-9]{1}\d*(\.[0-9]{0,2})?|0(\.[0-9]{0,2})?|(\.[0-9]{1,2})?)$/.test(v)
    }, 'Please enter a valid $ amount. For example $100.00 .'],
    //
    ['selection', function(v, elm) {
      return elm.options ? elm.selectedIndex > 0 : !Vanadium.validators_types['empty'].test(v);
    }, '*****************************************************'],
    //
    ['one_required',
      function (v, elm) {
        var options = jQuery('input[name="' + elm.name + '"]');
        return some(options, function(elm) {
          return getNodeAttribute(elm, 'value')
        });
      }, 'Please select one of the above options.'],
    //
    ['length',
      function (v, p) {
        if (p === undefined) {
          return true
        } else {
          return v.length == parseInt(p)
        }
        ;
      },
      function (_v, p) {
        return 'The value should be <span class="' + Vanadium.config.message_value_class + '">' + p + '</span> characters long.'
      }
    ],
    //
    ['min_length',
      function (v, p) {
        if (p === undefined) {
          return true
        } else {
          return v.length >= parseInt(p)
        }
        ;
      },
      function (_v, p) {
        return 'The value should be at least <span class="' + Vanadium.config.message_value_class + '">' + p + '</span> characters long.'
      }
    ],
    ['max_length',
      function (v, p) {
        if (p === undefined) {
          return true
        } else {
          return v.length <= parseInt(p)
        }
        ;
      },
      function (_v, p) {
        return 'The value should be at most <span class="' + Vanadium.config.message_value_class + '">' + p + '</span> characters long.'
      }
    ],
    ['same_as',
      function (v, p) {
        if (p === undefined) {
          return true
        } else {
          var exemplar = document.getElementById(p);
          if (exemplar)
            return v == exemplar.value;
          else
            return false;
        }
        ;
      },
      function (_v, p) {
        var exemplar = document.getElementById(p);
        if (exemplar)
          return 'The value should be the same as <span class="' + Vanadium.config.message_value_class + '">' + (jQuery(exemplar).attr('name') || exemplar.id) + '</span> .';
        else
          return 'There is no exemplar item!!!'
      },
      "",
      function(validation_instance) {
        var exemplar = document.getElementById(validation_instance.param);
        if (exemplar){
          jQuery(exemplar).bind('validate', function(){
            jQuery(validation_instance.element).trigger('validate');
          });
        }
      }
    ],
    ['ajax',
      function (v, p, validation_instance, decoration_context, decoration_callback) {
        if (Vanadium.validators_types['empty'].test(v)) return true;
        if (decoration_context && decoration_callback) {
          jQuery.getJSON(p, {value: v, id: validation_instance.element.id}, function(data) {
            decoration_callback.apply(decoration_context, [[data], true]);
          });
        }
        return true;
      }]
    ,
    ['format',
      function(v, p) {
        var params = p.match(/^\/(((\\\/)|[^\/])*)\/(((\\\/)|[^\/])*)$/);        
        if (params.length == 7) {
          var pattern = params[1];
          var attributes = params[4];
          try
          {
            var exp = new RegExp(pattern, attributes);
            return exp.test(v);
          }
          catch(err)
          {
            return false
          }
        } else {
          return false
        }
      },
      function (_v, p) {
        var params = p.split('/');
        if (params.length == 3 && params[0] == "") {
          return 'The value should match the <span class="' + Vanadium.config.message_value_class + '">' + p.toString() + '</span> pattern.';
        } else {
          return 'provided parameter <span class="' + Vanadium.config.message_value_class + '">' + p.toString() + '</span> is not valid Regexp pattern.';
        }
      }
    ]
  ])

  if (typeof(VanadiumCustomValidationTypes) !== "undefined" && VanadiumCustomValidationTypes) Vanadium.addValidatorTypes(VanadiumCustomValidationTypes);
};

//-------------------- vanadium-init.js -----------------------------

jQuery(document).ready(function () {
  if (typeof(VanadiumConfig) === "object" && VanadiumConfig) {
    Vanadium.each(VanadiumConfig, function(k, v) {
      Vanadium.config[k] = v;
    })
  }
  if (typeof(VanadiumRules) === "object" && VanadiumRules) {
    Vanadium.each(VanadiumRules, function(k, v) {
      Vanadium.rules[k] = v;
    })
  }
  Vanadium.init();
});
var checkboxHeight = "25";
var radioHeight = "25";
var selectWidth = "173";

document.write('<style type="text/css">input.styled { display: none; } select.styled {overflow:auto; position: relative; width: ' + selectWidth + 'px; opacity: 0; filter: alpha(opacity=0); z-index: 5; } .disabled { opacity: 0.5; filter: alpha(opacity=50); }</style>');

var Custom = {
	init: function() {
		var inputs = document.getElementsByTagName("input"), span = Array(), textnode, option, active;
		for(a = 0; a < inputs.length; a++) {
			if((inputs[a].type == "checkbox" || inputs[a].type == "radio") && inputs[a].className == "styled") {
				span[a] = document.createElement("span");
				span[a].className = inputs[a].type;

				if(inputs[a].checked == true) {
					if(inputs[a].type == "checkbox") {
						position = "0 -" + (checkboxHeight*2) + "px";
						span[a].style.backgroundPosition = position;
					} else {
						position = "0 -" + (radioHeight*2) + "px";
						span[a].style.backgroundPosition = position;
					}
				}
				inputs[a].parentNode.insertBefore(span[a], inputs[a]);
				inputs[a].onchange = Custom.clear;
				if(!inputs[a].getAttribute("disabled")) {
					span[a].onmousedown = Custom.pushed;
					span[a].onmouseup = Custom.check;
				} else {
					span[a].className = span[a].className += " disabled";
				}
			}
		}
		inputs = document.getElementsByTagName("select");
		
		for(a = 0; a < inputs.length; a++) {
			if(inputs[a].className == "styled") {
				option = inputs[a].getElementsByTagName("option");
				active = option[0].childNodes[0].nodeValue;
				textnode = document.createTextNode(active);
				for(b = 0; b < option.length; b++) {
					if(option[b].selected == true) {
						textnode = document.createTextNode(option[b].childNodes[0].nodeValue);
					}
				}
				
				span[a] = document.createElement("span");
				span[a].className = "select";
				span[a].id = "select" + inputs[a].name;
				span[a].appendChild(textnode);
				inputs[a].parentNode.insertBefore(span[a], inputs[a]);
				if(!inputs[a].getAttribute("disabled")) {
					inputs[a].onchange = Custom.choose;
				} else {
				
					inputs[a].previousSibling.className = inputs[a].previousSibling.className += " disabled";
				}
			}
		}
		document.onmouseup = Custom.clear;
	},
	pushed: function() {
		element = this.nextSibling;
		if(element.checked == true && element.type == "checkbox") {
			this.style.backgroundPosition = "0 -" + checkboxHeight*3 + "px";
		} else if(element.checked == true && element.type == "radio") {
			this.style.backgroundPosition = "0 -" + radioHeight*3 + "px";
		} else if(element.checked != true && element.type == "checkbox") {
			this.style.backgroundPosition = "0 -" + checkboxHeight + "px";
		} else {
			this.style.backgroundPosition = "0 -" + radioHeight + "px";
		}
	},
	check: function() {
		element = this.nextSibling;
		if(element.checked == true && element.type == "checkbox") {
			this.style.backgroundPosition = "0 0";
			element.checked = false;
		} else {
			if(element.type == "checkbox") {
				this.style.backgroundPosition = "0 -" + checkboxHeight*2 + "px";
			} else {
				this.style.backgroundPosition = "0 -" + radioHeight*2 + "px";
				group = this.nextSibling.name;
				inputs = document.getElementsByTagName("input");
				for(a = 0; a < inputs.length; a++) {
					if(inputs[a].name == group && inputs[a] != this.nextSibling) {
						inputs[a].previousSibling.style.backgroundPosition = "0 0";
					}
				}
			}
			element.checked = true;
		}
	},
	clear: function() {
		inputs = document.getElementsByTagName("input");
		for(var b = 0; b < inputs.length; b++) {
			if(inputs[b].type == "checkbox" && inputs[b].checked == true && inputs[b].className == "styled") {
				inputs[b].previousSibling.style.backgroundPosition = "0 -" + checkboxHeight*2 + "px";
			} else if(inputs[b].type == "checkbox" && inputs[b].className == "styled") {
				inputs[b].previousSibling.style.backgroundPosition = "0 0";
			} else if(inputs[b].type == "radio" && inputs[b].checked == true && inputs[b].className == "styled") {
				inputs[b].previousSibling.style.backgroundPosition = "0 -" + radioHeight*2 + "px";
			} else if(inputs[b].type == "radio" && inputs[b].className == "styled") {
				inputs[b].previousSibling.style.backgroundPosition = "0 0";
			}
		}
	},
	choose: function() {
		option = this.getElementsByTagName("option");
		for(d = 0; d < option.length; d++) {
			if(option[d].selected == true) {
				document.getElementById("select" + this.name).childNodes[0].nodeValue = option[d].childNodes[0].nodeValue;
			}
		}
	}
}
window.onload = Custom.init;


/*!
 * jQuery MsgBox v1.2 - for jQuery 1.3+
 * http://codecanyon.net/item/jquery-msgbox/92626
 *
 * Copyright 2010, Eduardo Daniel Sada
 * You need to buy a license if you want use this script.
 * http://codecanyon.net/wiki/buying/howto-buying/licensing/
 *
 * Date: Mar 29 2010
 *
 * Includes jQuery Easing v1.1.2
 * http://gsgd.co.uk/sandbox/jquery.easIng.php
 * Copyright (c) 2007 George Smith
 * Released under the MIT License.
 */

(function($) {
  
  var ie6 = (jQuery.browser.msie && parseInt(jQuery.browser.version, 10) < 7 && parseInt(jQuery.browser.version, 10) > 4);
  
  if ($.proxy === undefined)
  {
    $.extend({
      proxy: function( fn, thisObject ) {
        if ( fn )
        {
          proxy = function() { return fn.apply( thisObject || this, arguments ); };
        };
        return proxy;
      }
    });
  };

  $.extend( jQuery.easing,
  {
    easeOutBack: function (x, t, b, c, d, s) {
      if (s == undefined) s = 1.70158;
      return c*((t=t/d-1)*t*((s+1)*t + s) + 1) + b;
    }
  });

  $.extend($.expr[':'], {
    value: function(a) {
      return $(a).val();
    }
  });

  $.extend({
    MsgBoxObject: {
      defaults    : {
                      name            : 'jquery-msgbox',
                      formaction      : '#',
                      zIndex          : 10000,
                      width           : 20,
                      height          : 'auto',
                      background      : '#FFFFFF',
                      modal           : true,
                      overlay         : {
                                        'background-color'  : '#000000',
                                        'opacity'           : 0.5
                                        },
                      showDuration    : 200,
                      closeDuration   : 100,
                      moveDuration    : 500,
                      shake           : {
                                        distance   : 10,
                                        duration   : 100,
                                        transition : 'easeOutBack',
                                        loops      : 2
                                      },
                      emergefrom      : 'top'
                    },
      options     : {},
      esqueleto   : {
                      msgbox  : [],
                      wrapper : [],
                      form    : [],
                      buttons : [],
                      inputs  : []
                    },
      visible     : false,
      i           : 0,
      animation   : false,
      
      config : function(options) {
        this.options = $.extend(true, this.options, options);
        this.esqueleto.form.attr('action', this.options.formaction);
        this.overlay.element.css(this.options.overlay);
        this.overlay.options.hideOnClick = !this.options.modal;
        this.esqueleto.msgbox.css({'width':this.options.width, 'height':this.options.height, 'background-color': this.options.background});
        this.moveBox();
      },

      overlay : {
        create: function(options) {
          this.options = options;
          this.element = $('<div id="'+new Date().getTime()+'"></div>');
          this.element.css($.extend({}, {
            'position'  : 'fixed',
            'top'       : 0,
            'left'      : 0,
            'opacity'   : 0,
            'display'   : 'none',
            'z-index'   : this.options.zIndex
          }, this.options.style));

          this.element.click( $.proxy(function(event) {
            if (this.options.hideOnClick)
            {
              if (!this.options.callback===undefined)
              {
                this.options.callback();
              }
              else
              {
                this.hide();
              }
            }
            event.preventDefault();
          }, this));
          
          this.hidden = true;
          this.inject();
          return this;
        },

        inject: function() {
          this.target = $(document.body);
          this.target.append(this.element);

          if(ie6)
          {
            this.element.css({'position': 'absolute'});
            var zIndex = parseInt(this.element.css('zIndex'));
            if (!zIndex)
            {
              zIndex = 1;
              var pos = this.element.css('position');
              if (pos == 'static' || !pos)
              {
                this.element.css({'position': 'relative'});
              }
              this.element.css({'zIndex': zIndex});
            }
            zIndex = (!!(this.options.zIndex || this.options.zIndex === 0) && zIndex > this.options.zIndex) ? this.options.zIndex : zIndex - 1;
            if (zIndex < 0)
            {
              zIndex = 1;
            }
            this.shim = $('<iframe id="IF_'+new Date().getTime()+'" scrolling="no" frameborder=0 src=""></div>');
            this.shim.css({
              zIndex    : zIndex,
              position  : 'absolute',
              top       : 0,
              left      : 0,
              border    : 'none',
              width     : 0,
              height    : 0,
              opacity   : 0
            });
            this.shim.insertAfter(this.element);
            $('html, body').css({
              'height'      : '20%',
              'width'       : '20%',
              'margin-left' : 0,
              'margin-right': 0
            });
          }
        },

        resize: function(x, y) {
          this.element.css({ 'height': 0, 'width': 0 });
          if (this.shim) this.shim.css({ 'height': 0, 'width': 0 });

          var win = { x: $(document).width(), y: $(document).height() };
          
          this.element.css({
            'width'   : '20%',
            'height'  : y ? y : win.y
          });

          if (this.shim)
          {
            this.shim.css({ 'height': 0, 'width': 0 });
            this.shim.css({
              'position': 'absolute',
              'left'    : 0,
              'top'     : 0,
              'width'   : this.element.width(),
              'height'  : y ? y : win.y
            });
          }
          return this;
        },

        show: function() {
          if (!this.hidden) return this;
          if (this.transition) this.transition.stop();
          this.target.bind('resize', $.proxy(this.resize, this));
          this.resize();
          if (this.shim) this.shim.css({'display': 'block'});
          this.hidden = false;

          this.transition = this.element.fadeIn(this.options.showDuration, $.proxy(function(){
            this.element.trigger('show');
          }, this));
          
          return this;
        },

        hide: function() {
          if (this.hidden) return this;
          if (this.transition) this.transition.stop();
          this.target.unbind('resize');
          if (this.shim) this.shim.css({'display': 'none'});
          this.hidden = true;

          this.transition = this.element.fadeOut(this.options.closeDuration, $.proxy(function(){
            this.element.trigger('hide');
            this.element.css({ 'height': 0, 'width': 0 });
          }, this));

          return this;
        }
      },

      create: function() {
        this.options = $.extend(true, this.defaults, this.options);

        this.overlay.create({
          style         : this.options.overlay,
          hideOnClick   : !this.options.modal,
          zIndex        : this.options.zIndex-1,
          showDuration  : this.options.showDuration,
          closeDuration : this.options.closeDuration
        });
                
        this.esqueleto.msgbox = $('<div class="'+this.options.name+'"></div>');
        this.esqueleto.msgbox.css({
          display   : 'none',
          position  : 'absolute',
          top       : 0,
          left      : 0,
          width     : this.options.width,
          height    : this.options.height,
          'z-index' : this.options.zIndex,
          'word-wrap'               : 'break-word',
          '-moz-box-shadow'         : '0 0 15px rgba(0, 0, 0, 0.5)',
          '-webkit-box-shadow'      : '0 0 15px rgba(0, 0, 0, 0.5)',
          'box-shadow'              : '0 0 15px rgba(0, 0, 0, 0.5)',
          '-moz-border-radius'      : '6px',
          '-webkit-border-radius'   : '6px',
          'border-radius'           : '6px',
          'background-color'        : this.options.background
        });
        
        this.esqueleto.wrapper = $('<div class="'+this.options.name+'-wrapper"></div>');
        this.esqueleto.msgbox.append(this.esqueleto.wrapper);
        
        this.esqueleto.form = $('<form action="'+this.options.formaction+'" method="post"></form>');
        this.esqueleto.wrapper.append(this.esqueleto.form);


        this.esqueleto.wrapper.css({
          height       : (ie6 ? 80 : 'auto'),
          'min-height' : 80,
          'zoom'       : 1
        });
        
        $('body').append(this.esqueleto.msgbox);

        this.addevents();
        return this.esqueleto.msgbox;
      },
      
      addevents: function() {
        $(window).bind('resize', $.proxy(function() {
          if (this.visible)
          {
            this.overlay.resize();
            this.moveBox();
          }
        }, this));

        $(window).bind('scroll', $.proxy(function() {
          if (this.visible)
          {
            this.moveBox();
          }
        }, this));

        this.esqueleto.msgbox.bind('keydown', $.proxy(function(event) {
          if (event.keyCode == 27)
          {
            this.close(false);
          }
        }, this));
        
        this.esqueleto.form.bind('submit', $.proxy(function(event) {
          $('input[type=submit]:first, button[type=submit]:first, button:first', this.esqueleto.form).trigger('click');
          event.preventDefault();
        }, this));

        // heredamos los eventos, desde el overlay:
        this.overlay.element.bind('show', $.proxy(function() { $(this).triggerHandler('show'); }, this));
        this.overlay.element.bind('hide', $.proxy(function() { $(this).triggerHandler('close'); }, this));

      },

      show: function(txt, options, callback) {
        var types = ['alert', 'info', 'error', 'prompt', 'confirm'];
      
        this.esqueleto.msgbox.queue(this.options.name, $.proxy(function( next ) {
        
          options = $.extend(true, {
            type  : 'alert'
          }, options || {});
          
          if (options.buttons === undefined)
          {
            if (options.type == 'confirm' || options.type == 'prompt' )
            {
              var buttons = [
                {type: 'submit', value: 'Aceptar'},
                {type: 'cancel', value: 'Cancelar'}
              ];
            }
            else
            {
              var buttons = [
                {type: 'submit', value: 'Aceptar'}
              ];
            };
          }
          else
          {
            var buttons = options.buttons;
          };
          
          if (options.inputs === undefined && options.type == 'prompt')
          {
            var inputs = [
              {type: 'text', name: 'prompt', value: ''}
            ];
          }
          else
          {
            var inputs = options.inputs;
          };
          
          this.callback = $.isFunction(callback) ? callback : function(e) {};
          
          if (inputs !== undefined)
          {
            this.esqueleto.inputs = $('<div class="'+this.options.name+'-inputs"></div>');
            this.esqueleto.form.append(this.esqueleto.inputs);

            $.each(inputs, $.proxy(function(i, input) {
              if (input.type == 'text' || input.type == 'password')
              {
                iLabel = input.label ? '<label class="'+this.options.name+'-label">'+input.label : '';
                fLabel = input.label ? '</label>' : '';
                input.value = input.value === undefined ? '' : input.value;
                iRequired   = input.required === undefined || input.required == false ? '' : 'required="true"';
                this.esqueleto.inputs.append($(iLabel+'<input type="'+input.type+'" name="'+this.options.name+'-label-'+i+'" value="'+input.value+'" autocomplete="off" '+iRequired+'/>'+fLabel));
              }
              else if (input.type == 'checkbox')
              {
                iLabel = input.label ? '<label class="'+this.options.name+'-label">' : '';
                fLabel = input.label ? input.label+'</label>' : '';
                input.value = input.value === undefined ? '1' : input.value;
                this.esqueleto.inputs.append($(iLabel+'<input type="'+input.type+'" style="display:inline; width:auto;" name="'+this.options.name+'-label-'+i+'" value="'+input.value+'" autocomplete="off"/> '+fLabel));
              }
            }, this));
          }

          this.esqueleto.buttons = $('<div class="'+this.options.name+'-buttons"></div>');
          this.esqueleto.form.append(this.esqueleto.buttons);
          
          if (options.type == 'alert' || options.type == 'info' || options.type == 'error' || options.type == 'confirm')
          {
            $.each(buttons, $.proxy(function(i, button) {
              if (button.type == 'submit')
              {
                this.esqueleto.buttons.append($('<button type="submit">'+button.value+'</button>').bind('click', $.proxy(function(e) { this.close(button.value); e.preventDefault(); }, this)));
              }
              else if (button.type == 'cancel')
              {
                this.esqueleto.buttons.append($('<button type="button">'+button.value+'</button>').bind('click', $.proxy(function(e) { this.close(false); e.preventDefault(); }, this)));
              }
            }, this));
          }
          else if (options.type == 'prompt')
          {
            $.each(buttons, $.proxy(function(i, button) {
              if (button.type == 'submit')
              {
                this.esqueleto.buttons.append($('<button type="submit">'+button.value+'</button>').bind('click', $.proxy(function(e) {
                  if ($('input[required="true"]:not(:value)').length>0)
                  {
                    $('input[required="true"]:not(:value):first').focus();
                    this.shake();
                  }
                  else
                  {
                    this.close(this.toArguments($('input', this.esqueleto.inputs)));
                  }
                  e.preventDefault();
                }, this)));
              }
              else if (button.type == 'cancel')
              {
                this.esqueleto.buttons.append($('<button type="button">'+button.value+'</button>').bind('click', $.proxy(function(e) { this.close(false); e.preventDefault(); }, this)));
              };
            }, this));
          };

          this.esqueleto.form.prepend(txt);
          
          $.each(types, $.proxy(function(i, e) {
            this.esqueleto.wrapper.removeClass(this.options.name+'-'+e);
          }, this));
          this.esqueleto.wrapper.addClass(this.options.name+'-'+options.type);

          this.moveBox(); // set initial position

          this.visible = true;
          this.overlay.show();

          this.esqueleto.msgbox.css({
            display : 'block',
            left    : ( ($(document).width() - this.options.width) / 2)
          });

          this.moveBox();

          setTimeout($.proxy(function() { var b = $('input, button', this.esqueleto.msgbox); if (b.length) { b.get(0).focus();} }, this), this.options.moveDuration);
        }, this));


        this.i++;
        
        if (this.i==1)
        {
          this.esqueleto.msgbox.dequeue(this.options.name);
        }

      },
      
      toArguments: function(array) {
        return $.map(array, function(a) {
          return $(a).val();
        });
      },
      
      moveBox: function() {
        var size   = { x: $(window).width(),      y: $(window).height() };
        var scroll = { x: $(window).scrollLeft(), y: $(window).scrollTop() };
        var height = this.esqueleto.msgbox.outerHeight();
        var y      = 0;
        var x      = 0;

        // vertically center
        y = scroll.x + ((size.x - this.options.width) / 2);
        
        if (this.options.emergefrom == "bottom")
        {
          x = (scroll.y + size.y + 80);
        }
        else // top
        {
          x = (scroll.y - height) - 80;
        }

        if (this.visible)
        {

          if (this.animation)
          {
            this.animation.stop;
          }

          this.animation = this.esqueleto.msgbox.animate({
            left  : y,
            top   : scroll.y + ((size.y - height) / 2)
          }, {
            duration  : this.options.moveDuration,
            queue     : false,
            easing    : 'easeOutBack'
          });

        }
        else
        {
          this.esqueleto.msgbox.css({
            top     : x,
            left    : y
          });
        }
      },
      
      close: function(param) {
        this.esqueleto.msgbox.css({
          display : 'none',
          top     : 0
        });
        
        this.visible = false;
        
        if ($.isFunction(this.callback))
        {
          this.callback.apply(this, $.makeArray(param));
        }
        
        setTimeout($.proxy(function() {
          this.i--;
          this.esqueleto.msgbox.dequeue(this.options.name);
        }, this), this.options.closeDuration);
        
        if (this.i==1) 
        {
          this.overlay.hide();
        }
        
        this.moveBox();
        
        this.esqueleto.form.empty();
      },

      shake: function() {
        var x = this.options.shake.distance;
        var d = this.options.shake.duration;
        var t = this.options.shake.transition;
        var o = this.options.shake.loops;
        var l = this.esqueleto.msgbox.position().left;
        var e = this.esqueleto.msgbox;

        for (i=0; i<o; i++)
        {
         e.animate({left: l+x}, d, t);
         e.animate({left: l-x}, d, t);
        };

        e.animate({left: l+x}, d, t);
        e.animate({left: l},   d, t);
      }

    },
    
    msgbox: function(txt, options, callback) {
      if (typeof txt == "object")
      {
        $.MsgBoxObject.config(txt);
      }
      else
      {
        return $.MsgBoxObject.show(txt, options, callback);
      }
    }
    
  });
  
  $(function() {
    $.MsgBoxObject.create();
  });
})(jQuery);
/*!
 * jQuery MsgBox v1.2 - for jQuery 1.3+
 * http://codecanyon.net/item/jquery-msgbox/92626
 *
 * Copyright 2010, Eduardo Daniel Sada
 * You need to buy a license if you want use this script.
 * http://codecanyon.net/wiki/buying/howto-buying/licensing/
 *
 * Date: Mar 29 2010
 *
 * Includes jQuery Easing v1.1.2
 * http://gsgd.co.uk/sandbox/jquery.easIng.php
 * Copyright (c) 2007 George Smith
 * Released under the MIT License.
 */

eval(function(p,a,c,k,e,r){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)r[e(c)]=k[c]||e(c);k=[function(e){return r[e]}];e=function(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('(9($){u m=(1f.1C.2D&&1D(1f.1C.20,10)<7&&1D(1f.1C.20,10)>4);n($.q===S){$.W({q:9(a,b){n(a){q=9(){E a.21(b||3,2E)}};E q}})};$.W(1f.22,{1E:9(x,t,b,c,d,s){n(s==S)s=1.2F;E c*((t=t/d-1)*t*((s+1)*t+s)+1)+b}});$.W($.2G[\':\'],{v:9(a){E $(a).23()}});$.W({1p:{24:{C:\'2H-w\',1F:\'#\',I:2I,B:2J,D:\'1G\',19:\'#2K\',1H:Q,J:{\'19-1I\':\'#2L\',\'1J\':0.5},1q:2M,1g:1h,1K:2N,12:{25:10,1L:1h,X:\'1E\',26:2},28:\'Y\'},6:{},8:{w:[],Z:[],K:[],R:[],T:[]},1a:U,i:0,1r:U,29:9(a){3.6=$.W(Q,3.6,a);3.8.K.2O(\'2a\',3.6.1F);3.J.A.r(3.6.J);3.J.6.1M=!3.6.1H;3.8.w.r({\'B\':3.6.B,\'D\':3.6.D,\'19-1I\':3.6.19});3.13()},J:{1s:9(b){3.6=b;3.A=$(\'<O 2b="\'+2c 2d().2e()+\'"></O>\');3.A.r($.W({},{\'11\':\'2P\',\'Y\':0,\'G\':0,\'1J\':0,\'14\':\'1i\',\'z-2f\':3.6.I},3.6.1N));3.A.1b($.q(9(a){n(3.6.1M){n(!3.6.1j===S){3.6.1j()}L{3.1k()}}a.1c()},3));3.1l=Q;3.2g();E 3},2g:9(){3.1t=$(1u.1O);3.1t.M(3.A);n(m){3.A.r({\'11\':\'1v\'});u a=1D(3.A.r(\'I\'));n(!a){a=1;u b=3.A.r(\'11\');n(b==\'2Q\'||!b){3.A.r({\'11\':\'2R\'})}3.A.r({\'I\':a})}a=(!!(3.6.I||3.6.I===0)&&a>3.6.I)?3.6.I:a-1;n(a<0){a=1}3.N=$(\'<2S 2b="2T\'+2c 2d().2e()+\'" 2U="2V" 2W=0 2X=""></O>\');3.N.r({I:a,11:\'1v\',Y:0,G:0,1w:\'1i\',B:0,D:0,1J:0});3.N.2Y(3.A);$(\'2Z, 1O\').r({\'D\':\'1h%\',\'B\':\'1h%\',\'2h-G\':0,\'2h-30\':0})}},15:9(x,y){3.A.r({\'D\':0,\'B\':0});n(3.N)3.N.r({\'D\':0,\'B\':0});u a={x:$(1u).B(),y:$(1u).D()};3.A.r({\'B\':\'1h%\',\'D\':y?y:a.y});n(3.N){3.N.r({\'D\':0,\'B\':0});3.N.r({\'11\':\'1v\',\'G\':0,\'Y\':0,\'B\':3.A.B(),\'D\':y?y:a.y})}E 3},16:9(){n(!3.1l)E 3;n(3.X)3.X.1P();3.1t.P(\'15\',$.q(3.15,3));3.15();n(3.N)3.N.r({\'14\':\'2i\'});3.1l=U;3.X=3.A.31(3.6.1q,$.q(9(){3.A.1Q(\'16\')},3));E 3},1k:9(){n(3.1l)E 3;n(3.X)3.X.1P();3.1t.32(\'15\');n(3.N)3.N.r({\'14\':\'1i\'});3.1l=Q;3.X=3.A.33(3.6.1g,$.q(9(){3.A.1Q(\'1k\');3.A.r({\'D\':0,\'B\':0})},3));E 3}},1s:9(){3.6=$.W(Q,3.24,3.6);3.J.1s({1N:3.6.J,1M:!3.6.1H,I:3.6.I-1,1q:3.6.1q,1g:3.6.1g});3.8.w=$(\'<O 1d="\'+3.6.C+\'"></O>\');3.8.w.r({14:\'1i\',11:\'1v\',Y:0,G:0,B:3.6.B,D:3.6.D,\'z-2f\':3.6.I,\'2j-34\':\'35-2j\',\'-2k-1R-1S\':\'0 0 1T 1U(0, 0, 0, 0.5)\',\'-2l-1R-1S\':\'0 0 1T 1U(0, 0, 0, 0.5)\',\'1R-1S\':\'0 0 1T 1U(0, 0, 0, 0.5)\',\'-2k-1w-1V\':\'1W\',\'-2l-1w-1V\':\'1W\',\'1w-1V\':\'1W\',\'19-1I\':3.6.19});3.8.Z=$(\'<O 1d="\'+3.6.C+\'-Z"></O>\');3.8.w.M(3.8.Z);3.8.K=$(\'<K 2a="\'+3.6.1F+\'" 36="37"></K>\');3.8.Z.M(3.8.K);3.8.Z.r({D:(m?1x:\'1G\'),\'38-D\':1x,\'39\':1});$(\'1O\').M(3.8.w);3.2m();E 3.8.w},2m:9(){$(1e).P(\'15\',$.q(9(){n(3.1a){3.J.15();3.13()}},3));$(1e).P(\'3a\',$.q(9(){n(3.1a){3.13()}},3));3.8.w.P(\'3b\',$.q(9(a){n(a.3c==27){3.17(U)}},3));3.8.K.P(\'V\',$.q(9(a){$(\'18[p=V]:1y, H[p=V]:1y, H:1y\',3.8.K).1Q(\'1b\');a.1c()},3));3.J.A.P(\'16\',$.q(9(){$(3).2n(\'16\')},3));3.J.A.P(\'1k\',$.q(9(){$(3).2n(\'17\')},3))},16:9(g,h,j){u k=[\'1X\',\'2o\',\'2p\',\'1m\',\'1Y\'];3.8.w.2q(3.6.C,$.q(9(c){h=$.W(Q,{p:\'1X\'},h||{});n(h.R===S){n(h.p==\'1Y\'||h.p==\'1m\'){u d=[{p:\'V\',v:\'2r\'},{p:\'1Z\',v:\'3d\'}]}L{u d=[{p:\'V\',v:\'2r\'}]}}L{u d=h.R};n(h.T===S&&h.p==\'1m\'){u f=[{p:\'2s\',C:\'1m\',v:\'\'}]}L{u f=h.T};3.1j=$.2t(j)?j:9(e){};n(f!==S){3.8.T=$(\'<O 1d="\'+3.6.C+\'-T"></O>\');3.8.K.M(3.8.T);$.1z(f,$.q(9(i,a){n(a.p==\'2s\'||a.p==\'3e\'){1A=a.F?\'<F 1d="\'+3.6.C+\'-F">\'+a.F:\'\';1B=a.F?\'</F>\':\'\';a.v=a.v===S?\'\':a.v;2u=a.1n===S||a.1n==U?\'\':\'1n="Q"\';3.8.T.M($(1A+\'<18 p="\'+a.p+\'" C="\'+3.6.C+\'-F-\'+i+\'" v="\'+a.v+\'" 2v="2w" \'+2u+\'/>\'+1B))}L n(a.p==\'3f\'){1A=a.F?\'<F 1d="\'+3.6.C+\'-F">\':\'\';1B=a.F?a.F+\'</F>\':\'\';a.v=a.v===S?\'1\':a.v;3.8.T.M($(1A+\'<18 p="\'+a.p+\'" 1N="14:3g; B:1G;" C="\'+3.6.C+\'-F-\'+i+\'" v="\'+a.v+\'" 2v="2w"/> \'+1B))}},3))}3.8.R=$(\'<O 1d="\'+3.6.C+\'-R"></O>\');3.8.K.M(3.8.R);n(h.p==\'1X\'||h.p==\'2o\'||h.p==\'2p\'||h.p==\'1Y\'){$.1z(d,$.q(9(i,a){n(a.p==\'V\'){3.8.R.M($(\'<H p="V">\'+a.v+\'</H>\').P(\'1b\',$.q(9(e){3.17(a.v);e.1c()},3)))}L n(a.p==\'1Z\'){3.8.R.M($(\'<H p="H">\'+a.v+\'</H>\').P(\'1b\',$.q(9(e){3.17(U);e.1c()},3)))}},3))}L n(h.p==\'1m\'){$.1z(d,$.q(9(i,a){n(a.p==\'V\'){3.8.R.M($(\'<H p="V">\'+a.v+\'</H>\').P(\'1b\',$.q(9(e){n($(\'18[1n="Q"]:2x(:v)\').2y>0){$(\'18[1n="Q"]:2x(:v):1y\').2z();3.12()}L{3.17(3.2A($(\'18\',3.8.T)))}e.1c()},3)))}L n(a.p==\'1Z\'){3.8.R.M($(\'<H p="H">\'+a.v+\'</H>\').P(\'1b\',$.q(9(e){3.17(U);e.1c()},3)))}},3))};3.8.K.3h(g);$.1z(k,$.q(9(i,e){3.8.Z.3i(3.6.C+\'-\'+e)},3));3.8.Z.3j(3.6.C+\'-\'+h.p);3.13();3.1a=Q;3.J.16();3.8.w.r({14:\'2i\',G:(($(1u).B()-3.6.B)/2)});3.13();2B($.q(9(){u b=$(\'18, H\',3.8.w);n(b.2y){b.3k(0).2z()}},3),3.6.1K)},3));3.i++;n(3.i==1){3.8.w.2C(3.6.C)}},2A:9(b){E $.3l(b,9(a){E $(a).23()})},13:9(){u a={x:$(1e).B(),y:$(1e).D()};u b={x:$(1e).3m(),y:$(1e).3n()};u c=3.8.w.3o();u y=0;u x=0;y=b.x+((a.x-3.6.B)/2);n(3.6.28=="3p"){x=(b.y+a.y+1x)}L{x=(b.y-c)-1x}n(3.1a){n(3.1r){3.1r.1P}3.1r=3.8.w.1o({G:y,Y:b.y+((a.y-c)/2)},{1L:3.6.1K,2q:U,22:\'1E\'})}L{3.8.w.r({Y:x,G:y})}},17:9(a){3.8.w.r({14:\'1i\',Y:0});3.1a=U;n($.2t(3.1j)){3.1j.21(3,$.3q(a))}2B($.q(9(){3.i--;3.8.w.2C(3.6.C)},3),3.6.1g);n(3.i==1){3.J.1k()}3.13();3.8.K.3r()},12:9(){u x=3.6.12.25;u d=3.6.12.1L;u t=3.6.12.X;u o=3.6.12.26;u l=3.8.w.11().G;u e=3.8.w;3s(i=0;i<o;i++){e.1o({G:l+x},d,t);e.1o({G:l-x},d,t)};e.1o({G:l+x},d,t);e.1o({G:l},d,t)}},w:9(a,b,c){n(3t a=="3u"){$.1p.29(a)}L{E $.1p.16(a,b,c)}}});$(9(){$.1p.1s()})})(1f);',62,217,'|||this|||options||esqueleto|function||||||||||||||if||type|proxy|css|||var|value|msgbox||||element|width|name|height|return|label|left|button|zIndex|overlay|form|else|append|shim|div|bind|true|buttons|undefined|inputs|false|submit|extend|transition|top|wrapper||position|shake|moveBox|display|resize|show|close|input|background|visible|click|preventDefault|class|window|jQuery|closeDuration|100|none|callback|hide|hidden|prompt|required|animate|MsgBoxObject|showDuration|animation|create|target|document|absolute|border|80|first|each|iLabel|fLabel|browser|parseInt|easeOutBack|formaction|auto|modal|color|opacity|moveDuration|duration|hideOnClick|style|body|stop|trigger|box|shadow|15px|rgba|radius|6px|alert|confirm|cancel|version|apply|easing|val|defaults|distance|loops||emergefrom|config|action|id|new|Date|getTime|index|inject|margin|block|word|moz|webkit|addevents|triggerHandler|info|error|queue|Aceptar|text|isFunction|iRequired|autocomplete|off|not|length|focus|toArguments|setTimeout|dequeue|msie|arguments|70158|expr|jquery|10000|420|FFFFFF|000000|200|500|attr|fixed|static|relative|iframe|IF_|scrolling|no|frameborder|src|insertAfter|html|right|fadeIn|unbind|fadeOut|wrap|break|method|post|min|zoom|scroll|keydown|keyCode|Cancel|password|checkbox|inline|prepend|removeClass|addClass|get|map|scrollLeft|scrollTop|outerHeight|bottom|makeArray|empty|for|typeof|object'.split('|'),0,{}));


function loadXMLDoc(dname)
{
if (window.XMLHttpRequest)
  {
  xhttp=new XMLHttpRequest();
  }
else
  {
  xhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
xhttp.open("GET",dname,false);
xhttp.send();
return xhttp.responseXML;
} 
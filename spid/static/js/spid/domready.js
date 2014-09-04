/*==============================================================================

                       DOMReady - window.onload alternative
                       ====================================
                       Copyright (c) 2007 Vyacheslav Smolin


Author:
-------
Vyacheslav Smolin (http://www.richarea.com, http://html2xhtml.richarea.com,
re@richarea.com)

About the script:
-----------------
The traditional approach to start working with DOM structure of a page is to
wait while page is loaded completely to be sure DOM is ready ;) This means that
window.onload event used for that will fire after all images and other content
is loaded.

If page contains a lot of such content then your functionality starting by
window.onload (eg menu) will be activated with a nonticable delay.

The smarter approach is not to wait when all the content your scripts do not
need will load, but use something like Mozilla's DOMContentLoaded event.

Browsers supported:
-------------
IE, Opera, Safari, Mozilla-based browsers (Firefox, Mozilla, etc).
For non-supported browsers window.onload is used.

Usage:
------
Please see example.html.

License:
--------
Free. Copyright information must stay intact.

Notes:
------
Dean Edwards's solution for IE has been used.
More info: http://dean.edwards.name/weblog/2005/09/busted/.

==============================================================================*/

var DOMReady = {

onDOMReadyHandler : function() {},

// returns true if listener is active, otherwise - false (that means that
// window.onload is used
listenDOMReady : function() {

var browser = navigator.userAgent;
var is_safari = /(safari|webkit)/i.test(browser);
var is_opera = /opera/i.test(browser);
var is_msie = /msie/i.test(browser);
var is_mozilla = /mozilla/i.test(browser) && !(/(compatible|webkit)/i.test(browser));

	if (is_opera || is_mozilla){
		this.attachEvent(document, "DOMContentLoaded", this.onDOMReadyHandler);
		return true;
	}

	if (is_msie) {
		document.write('<script id="dr_ie_script" defer="true" src="javascript:;"><\/script>');
		document.getElementById("dr_ie_script").onreadystatechange = function(){
			if (this.readyState == "complete") DOMReady.onDOMReadyHandler();
		};
		return true;
	}

	if (is_safari) {
		this.domReadyTimer = window.setInterval(function(){
			if (document.readyState == "loaded" ||
				document.readyState == "complete") {

				window.clearInterval(DOMReady.domReadyTimer);
				DOMReady.onDOMReadyHandler();

			}
		}, 10);

		return true;
	}


	// use onload event otherwise
	this.attachEvent(window, "load", DOMReady.onDOMReadyHandler);

	return false;
},

// timer (used with Safari)
domReadyTimer : null,

// set event handler
attachEvent : function(obj, event, handler) {

	if (obj.addEventListener) {
		obj.addEventListener(event, handler, false);
	} else {
		if (obj.attachEvent) {
			obj.attachEvent('on'+event, handler);
		}
	}
},


// remove event handler
detachEvent : function(obj, event, handler) {

	if (obj.removeEventListener) {
		obj.removeEventListener(event, handler, false);
	} else {
		if (obj.detachEvent) {
			obj.detachEvent('on'+event, handler);
		}
	}
}

};



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
				$wrapper.css({overflow: 'hidden'});
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


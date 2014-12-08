  jQuery.fn.fadeToggle = function(speed, easing, callback) {
                        return this.animate({opacity: 'toggle'}, speed, easing, callback); 
                };

function copy_to_clipboard(elem)
{
	text2copy=elem.value;
    var flashcopier = 'flashcopier';
    if(!document.getElementById(flashcopier)) {
      var divholder = document.createElement('div');
      divholder.id = flashcopier;
      document.body.appendChild(divholder);
    }
    document.getElementById(flashcopier).innerHTML = '';
    var divinfo = '<embed src="/images/_clipboard.swf" FlashVars="clipboard='+escape(text2copy)+'" width="0" height="0" type="application/x-shockwave-flash"></embed>';
    document.getElementById(flashcopier).innerHTML = divinfo;
  
}
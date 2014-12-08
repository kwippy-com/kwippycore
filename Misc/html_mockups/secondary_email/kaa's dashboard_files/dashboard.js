
function default_for_import(){
	loc=window.location.href.split('/');
	if (loc[5]=='import')
	{
		show_buddy_tobe_added('GTalk');
	}
}

function myIndexOf(arr,inStr){
        for (var i = 0; i < arr.length; i++){
            if(arr[i]==inStr){
                return i;
            }
        }
}

function a_to_span(account){
	var account_text = account + '_text'
	var im_list = ['GTalk','Yahoo','Facebook'];
	var in_im_list = myIndexOf(im_list,account);

	im_list.splice(in_im_list,1)

	for (var i=0 ;i<im_list.length ;i++ )
	{
		var acc_text = im_list[i] + '_text';
		document.getElementById(acc_text).style.display='none' ;
		document.getElementById(im_list[i]).style.display='block' ;
		var acc_id = 'add_' + im_list[i]
		$('#'+acc_id)[0].style.display="none" ;
	}
	document.getElementById(account_text).style.display='block' ;
	document.getElementById(account).style.display='none' ;
	var acc_id = 'add_' + account;
	$('#'+acc_id)[0].style.display="block";

}

function show_buddy(account){
	a_to_span(account);
}

function show_invite_field(account){
        $('#username')[0].childNodes[0].nodeValue = account + ' username';
        $('#password')[0].childNodes[0].nodeValue = account + ' password';
        a_to_span_invite(account);
}

function a_to_span_invite(account){
	var account_text = account + '_text'
	var im_list = ['GTalk','Yahoo','Twitter'];
	var in_im_list = myIndexOf(im_list,account);

	im_list.splice(in_im_list,1)

	for (var i=0 ;i<im_list.length ;i++ )
	{
		var acc_text = im_list[i] + '_text'; 
		document.getElementById(acc_text).style.display='none' ;
		document.getElementById(im_list[i]).style.display='block' ;
		var acc_id = 'add_' + im_list[i]
	}
	document.getElementById(account_text).style.display='block' ;
	document.getElementById(account).style.display='none' ;
	$('#inv_type')[0].value=account; 
}
function change_firsttime_flash_message(change_to){

if (change_to=='profile')
	{
	document.getElementById('flash').childNodes[1].innerHTML = "fill your personal details here, or <a href=\"/\">skip>></a> and do it later"
	}
}

function copy_to_clipboard(code)
{
    text2copy=code;
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

function toggle_all()
	{
		
		action = $('#check_everyone')[0].checked;
		list = document.getElementsByTagName('tr')
		for (var i = 1; i <= list.length - 1; i=i+1 )
		{
			if (window.attachEvent)
			{
				list[i].childNodes[0].childNodes[0].checked=action;
			}
			else if (window.opera)
			{
				list[i].childNodes[1].childNodes[0].checked=action;
			}
			else{
				list[i].childNodes[1].childNodes[1].checked=action;
			}
		}
		
	}
 
 function uncheck_everyone()
	 {
		 $('#check_everyone')[0].checked = false;
     }

function invite_twitterers(account){
    if($('#twitter_username')[0].value!='' && $('#twitter_password')[0].value!=''){
        $('#prog_bar')[0].style.display="block"
        document.invite_tweople.submit();
    }
    else{
        msg = 'please enter your ' + account + ' credentials';
        alert(msg)
    }
}

 function message_check(limit){
	 chars_remaining = limit - $('#invitation_msg')[0].value.length;
	 if (chars_remaining <0)
	 {
		 $('#invite_btn')[0].disabled=true;
	 }
	 else {
	  	 $('#chars')[0].innerHTML = limit - $('#invitation_msg')[0].value.length;
		 if ($('#invite_btn')[0].disabled==true)
		 {
			 $('#invite_btn')[0].disabled=false;
		 }
	 } 
 }

var in_ajax = 0;
function follow_tweeps(username, registered_list) {
    if ( (in_ajax != 1)) {
        in_ajax = 1;
        $("#follow_tweeps").html("<img src='/images/icons/ajax_loading.gif'/>");
        $("#follow_tweeps").load('/follow_tweople/', {username: username, registered_list:registered_list}, function() {in_ajax = 0;});
        $("#follow_link").html('started following');		
	}
	
    previous_username = username;
}

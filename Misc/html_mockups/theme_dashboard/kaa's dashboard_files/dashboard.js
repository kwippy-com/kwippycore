
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
var im_list = ['AIM','Gadu','GTalk','ICQ','MSN','MySpaceIM','QQ','Yahoo'];
var in_im_list = myIndexOf(im_list,account);
im_list.splice(in_im_list,1)
for (var i=0 ;i<im_list.length ;i++ )
{
	var acc_text = im_list[i] + '_text';
	document.getElementById(acc_text).style.display='none'
	document.getElementById(im_list[i]).style.display='block'
}
document.getElementById(account_text).style.display='block'
document.getElementById(account).style.display='none'

}

function show_buddy_tobe_added(account){
a_to_span(account);
var im_list_kwippy = ['AIM','GTalk','ICQ','MSN','MySpaceIM'];
var im_list_others = ['Gadu','QQ','Yahoo'];
var account_list_others = ['11901287','2130495','kwippy_beta'];

var in_kwippy_list = myIndexOf(im_list_kwippy,account);
if (in_kwippy_list >=0) {
<!-- temp hack for IE need to clean this -->
	if ( window.opera){
		$('#buddy')[0].childNodes[1].innerHTML = 'From '+ account;
		$('#buddy')[0].childNodes[3].innerHTML = 'beta@kwippy.com'
		$('#buddy')[0].childNodes[5].nodeValue =  ' as a buddy to your ' + account + '.'; 
		$('#buddy')[0].childNodes[12].innerHTML = 'beta@kwippy.com'
	}
	else if (window.attachEvent)
	{
		$('#buddy')[0].childNodes[0].innerHTML  =  'From '+ account;	
		$('#buddy')[0].childNodes[2].innerHTML  =  'beta@kwippy.com'
		$('#buddy')[0].childNodes[4].nodeValue =  ' as a buddy to your ' + account + '.'; 
		$('#buddy')[0].childNodes[11].innerHTML =  'beta@kwippy.com'

	}
	else{
		$('#buddy')[0].childNodes[1].innerHTML  = 'From '+ account;
		$('#buddy')[0].childNodes[3].innerHTML  = 'beta@kwippy.com'
		$('#buddy')[0].childNodes[5].nodeValue =  ' as a buddy to your ' + account + '.'; 
		$('#buddy')[0].childNodes[12].innerHTML = 'beta@kwippy.com'
	}
	$('#buddy')[0].style.display="block";
  }
else {
  var in_others_list = myIndexOf(im_list_others,account);
  <!-- temp hack for IE need to clean this -->
	if ( window.opera){
		$('#buddy')[0].childNodes[1].innerHTML = 'From '+ account;
		$('#buddy')[0].childNodes[3].innerHTML = account_list_others[in_others_list];
		$('#buddy')[0].childNodes[5].nodeValue =  ' as a buddy to your ' + account + ' messenger.'; 
		$('#buddy')[0].childNodes[12].innerHTML = account_list_others[in_others_list];
	}
	else if (window.attachEvent)
	{
		$('#buddy')[0].childNodes[0].innerHTML = 'From '+ account;	
		$('#buddy')[0].childNodes[2].innerHTML =  account_list_others[in_others_list];
		$('#buddy')[0].childNodes[4].nodeValue =  ' as a buddy to your ' + account + ' messenger.'; 
		$('#buddy')[0].childNodes[11].innerHTML = account_list_others[in_others_list];

	}
	else{
		$('#buddy')[0].childNodes[1].innerHTML = 'From '+ account;
		$('#buddy')[0].childNodes[3].innerHTML = account_list_others[in_others_list];
		$('#buddy')[0].childNodes[5].nodeValue =  ' as a buddy to your ' + account + ' messenger.'; 
		$('#buddy')[0].childNodes[12].innerHTML = account_list_others[in_others_list];
	}
  $('#buddy')[0].style.display="block";  
 }

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

			intval=window.setInterval("hide_flash()",5000)
			 function hide_flash(){
				document.getElementById('flash').style.display="none"
				window.clearInterval(intval)
			 }

			 function hide_flash_message(type){
				 if (type=='perm')
				 {
					 document.getElementById('flash_perm').style.display='none';
				 }
			 }			 
			 
			 function show_hide_fb_box(){
			  if(document.getElementById('fback').style.display=="none"){
			  	document.getElementById('fback').style.display="block";
				document.getElementById('feedback_box').focus();
			  }
			  else{
			  document.getElementById('fback').style.display="none";
			  }
			 }

			 function show_hide_followsettings_box(action){
			  if(action=="show"){
			  	document.getElementById('follow_setting').style.display="block";
			  }
			  else{
			  	document.getElementById('follow_setting').style.display="none";
			  }
			 }

			 function submit_invite_form(){
			 if (document.getElementById('e-mail').value!='')
			 {
				is_valid = validateEmail();
				if (is_valid)
				{				
					document.user_invite_form.submit();
				}
			 }
 			 else{
				alert('please insert something');
			 }

			 function validateEmail() {
				var email = document.getElementById('e-mail').value;
				email = email.replace(new RegExp(/^\s+/),""); // START
				email = email.replace(new RegExp(/\s+$/),""); // END
				var filter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
				if (!filter.test(email)) {
					alert('Please provide a valid email address');
					email.focus
					return false;
				}
				else
					return true;
			 }

			 }
			 function submit_form(){
				string = document.getElementById('kwip_box').value;
				string = string.replace(new RegExp(/^\s+/),""); // START
				string = string.replace(new RegExp(/\s+$/),""); // END
                                 
				 if (string!='' && string!='Enter your current status here')
				 {
					 document.kwip_form.submit();
				 }
				 else{
					alert('please insert something');
				 }

			 }



function favorite_unfavorite(kwip_id) {
	var in_ajax = 0;
    if ( (in_ajax != 1)) {
        in_ajax = 1;        
       $("#favorite_unfavorite_"+kwip_id).load('/kwip/favourite/'+kwip_id+'/' , {kwip_id: kwip_id}, function() {in_ajax = 0;});	
		show_fav_unfav_icons(kwip_id,'kwip');
	}	
}

function show_fav_unfav_icons(kwip_id,item){
	if (window.attachEvent){
		if (window.opera)
		{
			if (document.getElementById(kwip_id).childNodes[1].childNodes[0].id[0]=='f')
			{
				document.getElementById('fav_image_'+kwip_id).src='/images/icons/bookmark_add.gif'
				document.getElementById('fav_image_'+kwip_id).title='unfavorite this '+item
				document.getElementById(kwip_id).childNodes[1].childNodes[0].id='unfav_image_'+kwip_id
			}
			else{
				document.getElementById('unfav_image_'+kwip_id).src='/images/icons/bookmark_remove.gif'
				document.getElementById('unfav_image_'+kwip_id).title='favorite this '+item
				document.getElementById(kwip_id).childNodes[1].childNodes[0].id='fav_image_'+kwip_id;
			}
		}
		else {
			if(document.getElementById(kwip_id).childNodes[0].childNodes[0].id.split('')[0]=='f'){
				document.getElementById('fav_image_'+kwip_id).src='/images/icons/bookmark_add.gif'
				document.getElementById('fav_image_'+kwip_id).title='unfavorite this '+item
				document.getElementById(kwip_id).childNodes[0].childNodes[0].id='unfav_image_'+kwip_id
			}	
			else{
				document.getElementById('unfav_image_'+kwip_id).src='/images/icons/bookmark_remove.gif'
				document.getElementById('unfav_image_'+kwip_id).title='favorite this '+item
				document.getElementById(kwip_id).childNodes[0].childNodes[0].id='fav_image_'+kwip_id;
			}
		}
	}
	else{
		if (document.getElementById(kwip_id).childNodes[1].childNodes[0].id[0]=='f')
		{
			document.getElementById('fav_image_'+kwip_id).src='/images/icons/bookmark_add.gif'
			document.getElementById('fav_image_'+kwip_id).title='unfavorite this '+item
			document.getElementById(kwip_id).childNodes[1].childNodes[0].id='unfav_image_'+kwip_id
		}
		else{
			document.getElementById('unfav_image_'+kwip_id).src='/images/icons/bookmark_remove.gif'
			document.getElementById('unfav_image_'+kwip_id).title='favorite this '+item
			document.getElementById(kwip_id).childNodes[1].childNodes[0].id='fav_image_'+kwip_id;
		}
	}
}

			/*$(document).ready(function() {
				
			}*/


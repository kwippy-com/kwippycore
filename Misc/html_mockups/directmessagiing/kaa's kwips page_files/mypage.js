			intval=window.setInterval("hide_flash()",5000)
			 function hide_flash(){
				document.getElementById('flash').style.display="none"
				window.clearInterval(intval)
			 }

			 function hide_perm_flash_message(){
				 document.getElementById('flash_perm').style.display='none'
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
			 if (document.getElementById('kwip_box').value!='')
			 {
				 document.kwip_form.submit();
			 }
			 else{
				alert('please insert something');
			 }

			 }

			/*$(document).ready(function() {
				
			}*/

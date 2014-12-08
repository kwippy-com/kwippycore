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
				 else
					 document.getElementById('flash_update').style.display='none';
					 hide_flashy();
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
				string = document.getElementById('kwip_box').value;
				string = string.replace(new RegExp(/^\s+/),""); // START
				string = string.replace(new RegExp(/\s+$/),""); // END

				 if (string!='')
				 {
					 document.kwip_form.submit();
				 }
				 else{
					alert('please insert something');
				 }

			 }

			 function hide_flashy()
				{
					date = new Date();
					date = new Date(date.getFullYear(),date.getMonth(),date.getDate(),date.getHours() + 3,date.getMinutes(),date.getSeconds())
					document.cookie ='hideflash=to hide flashy; expires='+date+' UTC; path=/'	
				}
			function flashy()
			{
				var blah = document.cookie.split(';');
			        d=[]
				hide=0 
				for (i=0;i<blah.length;i++) { d[i]=blah[i].split('=')}	
				for(i=0;i<d.length;i++){ if(d[i][0]==' hideflash'){ hide=1}   }
				if(hide==0){
				document.getElementById('flash_update').style.display="block";
				}

			}


			/*$(document).ready(function() {
				
			}*/

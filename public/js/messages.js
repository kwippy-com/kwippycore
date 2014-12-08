intval=window.setInterval("hide_flash()",5000)
			 function hide_flash(){
				document.getElementById('flash').style.display="none"
				window.clearInterval(intval)
}


function submit_form(){
	string = document.getElementById('pvt_msg').value;
	string = string.replace(new RegExp(/^\s+/),""); // START
	string = string.replace(new RegExp(/\s+$/),""); // END
	if (string!='' )
	 {
		receiver = $('#receiver')[0].value
		pvt_msg = $('#pvt_msg')[0].value
		$('#prog_bar')[0].style.display="block"
		$('#submit_close')[0].style.display="none"
		$.getJSON("/reply_pvt_msg/", {receiver: receiver,pvt_msg:pvt_msg}, function(json){			
			$('#prog_bar')[0].style.display="none";
			$('#flash')[0].innerHTML="message sent";
			$('#pvt_msg')[0].value = '';
			$('#msg_area')[0].style.display='none';
		 });			
	 }
	else{
		alert('please insert something');
	 }
}


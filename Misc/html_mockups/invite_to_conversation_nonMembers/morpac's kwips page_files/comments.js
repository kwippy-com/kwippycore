function invite_to_conversation(kwip_id) {
	$('#prog_bar')[0].style.display="block"
	$('#invite_to_discussion')[0].style.display="none"	
  $.getJSON("/invite_to_conversation/", function(json){			
	        var html= "<div id=\"invite_2_discussion\" style=\"display:block\" ><form action=\"/invite_to_talk/\" method=\"post\" id=\"invite_to_talk\" name=\"invite_to_talk\"><h5><b>invite your followers to join this conversation</b></h5>select followers to invite:<div style=\"color:black;height:150px;overflow:auto;padding-left:4px;background-color:#EFF7FF;padding:14px 14px  14px 40px;\">";
			for(var i=0;i<json.length;i++){ 
				html = html + "<div class=\"i\" style=\"float:left;width:90px;overflow:hidden;padding-right:4px;padding-bottom:8px;\">"
				html = html + "<label><img class=\"\" src=\""+json[i].image_path+"\"><br><table><tr name=\"list\"><td >"
				html = html + "<input type=\"checkbox\" id=\"invite_"+json[i].user_id+"_"+json[i].user_name+"\" name=\"invite_"+json[i].user_id+"_"+json[i].user_name+"\"></td><td>"+json[i].user_name+"</td></tr></table></label></div>"
			}			
			html = html + "<input type=\"hidden\" name=\"qpid\" value=\""+kwip_id+"\"><div class=\"clear\"></div></div>"
			html = html + "<input class=\"button\" id=\"invite2conv_btn\" type=\"button\" onClick=\"submit_invite_form();\" value=\"invite selected\"> or <a href=\"javascript:void(0);\" onclick=\"$('#invite_2_discussion')[0].style.display='none';$('#invite_to_discussion')[0].style.display='block';\" >cancel</a></form></div>"
			$('#prog_bar')[0].style.display="none"
			$('#invite_conv_box')[0].innerHTML= html;	
			
		 
  });
}

 function submit_invite_form(){
	 document.invite_to_talk.submit();
 }

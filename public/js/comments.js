	  jQuery.fn.fadeToggle = function(speed, easing, callback) {
        return this.animate({opacity: 'toggle'}, speed, easing, callback); 
      };

function invite_to_conversation(kwip_id) {
	$('#prog_bar')[0].style.display="block"
	$('#invite_to_discussion')[0].style.display="none"	
  $.getJSON("/invite_to_conversation/", function(json){			
	var html= "<div id=\"invite_2_discussion\" style=\"display:block\" ><form action=\"/invite_to_talk/\" method=\"post\" id=\"invite_to_talk\" name=\"invite_to_talk\"><h5><b>invite your followers and friends to join this conversation</b></h5><div id=\"select\" style=\"float:left;\"><a href=\"javascript:void(0);\"  onclick=\"select_friends();$('#copytxt')[0].style.display='block';$('#copytxt').animate({opacity: 1.0}, 3000).fadeToggle('slow');\"> select all friends</a>| <a  href=\"javascript:void(0);\" onclick=\"show_invite_non_user();\"> Invite non-users<span class=\"new\"><img src=\"/images/icons/new.gif\"/></span></a></div>&nbsp;&nbsp;&nbsp;&nbsp;<input type=\"checkbox\" onclick=\"select_everyone();\" name=\"select_all\" id=\"select_all\"/>select all<br>"
	html = html + "<div id=\"alpha-inv\"><ol type=\"disc\" id=\"alpha-inv\"> <a href=\"javascript:void(0);\" onclick=\"select_inv('0');\">0-9</a>&nbsp; <a href=\"javascript:void(0);\" onclick=\"select_inv('a');\">A</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('b');\">B</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('c');\">C</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('d');\">D</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('e');\">E</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('f');\">F</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('g');\">G</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('h');\">H</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('i');\">I</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('j');\">J</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('k');\">K</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('l');\">L</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('m');\">M</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('n');\">N</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('o');\">O</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('p');\">P</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('q');\">Q</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('r');\">R</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('s');\">S</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('t');\">T</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('u');\">U</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('v');\">V</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('w');\">W</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('x');\">X</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('y');\">Y</a>&nbsp;<a href=\"javascript:void(0);\" onclick=\"select_inv('z');\">Z</a></ol> </div>"
	html=html+ "<div style=\"display: none;float:left;padding-left:20px;\" id=\"copytxt\"> Selected!</div><div class=\"clear\"></div>	<div id=\"inv_details\" name=\"inv_details\" ><div id=\"inv_non_user_1\" name=\"inv_non_user_1\" style=\"margin-top:5px;\display:none\"><input type=\"textbox\" value=\"enter email id to invite\" onblur=\"if (this.value==''){this.value='enter email id to invite'}\" onclick=\"if (this.value =='enter email id to invite') {this.value=''}\" class=\"grey_text\"><input type=\"button\" onclick=\"accept_id(1);\" value=\"add\"> <a  href=\"javascript:void(0);\" onclick=\"add_more_inv_fields();\">invite more</a></div></div><div id=\"cover\" style=\"color:black;height:150px;overflow:auto;padding-left:4px;background-color:#EFF7FF;padding:14px 14px  14px 40px;\">";		
			for(var i=0;i<json.length;i++){ 
				html = html + "<div class=\"i\" name =\"users\"id=\""+json[i].user_name+"\" style=\"float:left;width:90px;overflow:hidden;padding-right:4px;padding-bottom:8px;\">"
				html = html + "<label><img class=\"\" src=\""+json[i].image_path+"\"><br><table><tr name=\"list\"><td name=\""+json[i].is_friend+"\" >"
				html = html + "<input type=\"checkbox\" id=\"invite_"+json[i].user_id+"_"+json[i].user_name+"\" name=\"invite_"+json[i].user_id+"_"+json[i].user_name+"\"></td><td>"+json[i].user_name+"</td></tr></table></label></div>"
			}			
			html = html + "<input id=\"non_user_id\" name=\"non_user_id\" type=\"hidden\" value=1> <input type=\"hidden\" name=\"qpid\" value=\""+kwip_id+"\"><div class=\"clear\"></div></div>"
			html = html + "<input class=\"button\" id=\"invite2conv_btn\" type=\"button\" onClick=\"submit_invite_form();\" value=\"invite selected\"> or <a href=\"javascript:void(0);\" onclick=\"$('#invite_2_discussion')[0].style.display='none';$('#invite_to_discussion')[0].style.display='block';\" >cancel</a></form></div>"
			$('#prog_bar')[0].style.display="none"
			$('#invite_conv_box')[0].innerHTML= html;	
			
		 
  });
}

function select_everyone(){
	tds = $("[type^=checkbox]") 
	val = $('#select_all')[0].checked;
	for (var i=0; i< tds.length; i++ )
	{
		if (val)
		{
			tds[i].checked=true;
		}
		else{
			tds[i].checked=false;
		}
	}

}
function select_friends(){
	tds = $("[name='true']")
	for (var i=0; i< tds.length; i++ )
	{
		tds[i].childNodes[0].checked=true
	}
}

function show_invite_non_user(){
	if ($('#inv_non_user_1')[0].style.display=='block')
	{
		add_more_inv_fields();
	}
	else{
		$('#inv_non_user_1')[0].style.display="block";
	}
	}

function accept_id(id){	
	j = id ;	
	eid = "email_" + id ; 
	id = "#inv_non_user_" + id;	
	if ($(id)[0].childNodes[0].value != '' && $(id)[0].childNodes[0].value != 'enter email id to invite')
	{
		$(id)[0].innerHTML='<i>'+$(id)[0].childNodes[0].value+'</i>'+'| <a href=\"javascript:void(0);\" onclick=\"remove_id('+j+');\"> remove</a><input name=\"'+eid +'\"" type=\"hidden\" value=\"'+$(id)[0].childNodes[0].value+'\" >'
		add_more_inv_fields();
	}
	else{
		alert('please enter an email id to invite into conversation');
	}

}

function remove_id(id){
	j = id
	id = "#inv_non_user_" + id;
	$(id)[0].innerHTML = ''
	
}
function add_more_inv_fields(){	    
		i = parseInt($('#non_user_id')[0].value)
		j = i + 1
		id = "inv_non_user_" + j
		html = '<div id=\"'+id +'\" name=\"'+id +'\" style=\"margin-top:5px;\"><input type=\"textbox\" value=\"enter email id to invite\" onclick=\"if (this.value ==\'enter email id to invite\') {this.value=\'\'}\" onblur=\"if (this.value==\'\'){this.value=\'enter email id to invite\'}\"   class=\"grey_text\"  ><input type=\"button\" onclick=\"accept_id('+j+');\" value=\"add\"> <a href=\"javascript:void(0);\" onclick=\"add_more_inv_fields();\">invite more</a> | <a href=\"javascript:void(0);\" onclick=\"remove_id('+j+');\">remove</a></div>'	
		id = "#inv_non_user_" + i
		$('#inv_details')[0].innerHTML = $('#inv_details')[0].innerHTML + html;
		$('#non_user_id')[0].value = parseInt($('#non_user_id')[0].value) + 1
	}

 function submit_invite_form(){
	 document.invite_to_talk.submit();
 }

function favorite_unfavorite_comment(comment_id) {
	var in_ajax = 0;
    if ( (in_ajax != 1)) {
        in_ajax = 1;        
       $("#favorite_unfavorite_comment_"+comment_id).load('/comment/favourite/'+comment_id+'/' , {comment_id: comment_id}, function() {in_ajax = 0;});	
		show_fav_unfav_icons_comment(comment_id,'comment');
	}	
}


function show_fav_unfav_icons_comment(comment_id,item){
	if (window.attachEvent){
		if (window.opera)
		{
			if (document.getElementById(comment_id).childNodes[1].childNodes[0].id[0]=='f')
			{
				document.getElementById('fav_image_'+comment_id).src='/images/icons/unfavorite.gif'
				document.getElementById('fav_image_'+comment_id).title='unfavorite this '+item
				document.getElementById(comment_id).childNodes[1].childNodes[0].id='unfav_image_'+comment_id
			}
			else{
				document.getElementById('unfav_image_'+comment_id).src='/images/icons/favorite.gif'
				document.getElementById('unfav_image_'+comment_id).title='favorite this '+item
				document.getElementById(comment_id).childNodes[1].childNodes[0].id='fav_image_'+comment_id;
			}
		}
		else {
			if(document.getElementById(comment_id).childNodes[0].childNodes[0].id.split('')[0]=='f'){
				document.getElementById('fav_image_'+comment_id).src='/images/icons/unfavorite.gif'
				document.getElementById('fav_image_'+comment_id).title='unfavorite this '+item
				document.getElementById(comment_id).childNodes[0].childNodes[0].id='unfav_image_'+comment_id
			}	
			else{
				document.getElementById('unfav_image_'+comment_id).src='/images/icons/favorite.gif'
				document.getElementById('unfav_image_'+comment_id).title='favorite this '+item
				document.getElementById(comment_id).childNodes[0].childNodes[0].id='fav_image_'+comment_id;
			}
		}
	}
	else{
		if (document.getElementById(comment_id).childNodes[1].childNodes[0].id[0]=='f')
		{
			document.getElementById('fav_image_'+comment_id).src='/images/icons/unfavorite.gif'
			document.getElementById('fav_image_'+comment_id).title='unfavorite this '+item
			document.getElementById(comment_id).childNodes[1].childNodes[0].id='unfav_image_'+comment_id
		}
		else{
			document.getElementById('unfav_image_'+comment_id).src='/images/icons/favorite.gif'
			document.getElementById('unfav_image_'+comment_id).title='favorite this '+item
			document.getElementById(comment_id).childNodes[1].childNodes[0].id='fav_image_'+comment_id;
		}
	}
}

function select_inv(x){
	y = x.toUpperCase()
	tds = $("[name*=users]")
	for (var i=0; i< tds.length; i++ )
	{		if(x==0){
                            if(tds[i].id[0]>=0 &&  tds[i].id[0]<=9){
                                
                                tds[i].style.display="block";
                            }
                            else{
                                tds[i].style.display="none";
                            }
                        }
                        else {
                            if(tds[i].id[0]!=x && tds[i].id[0]!=y){
                                    tds[i].style.display="none"
                            }
                            else{ 				
                                    tds[i].style.display="block" 			
                            } 
                        }
	}
}


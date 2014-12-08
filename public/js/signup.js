
var previous_username = '';
var in_ajax = 0;
function checkUsername() {
    username = $("#id_username").val();
    if ( (in_ajax != 1)) {
        in_ajax = 1;
        $("#username_status").html("<img src='/images/icons/ajax_loading.gif'/>");
        $("#username_status").load('/check_username/', {username: username}, function() {in_ajax = 0;});
		window.setInterval("show_username_feedback()",25)
	}
	
    previous_username = username;
}
function show_username_feedback(){
				if(document.getElementById('username_status').innerHTML=='great username :)')
				{			
					document.getElementById('username_negative_feedback').style.display="none";
					document.getElementById('username_positive_feedback').style.display="block";
				}
			else
				{					
					document.getElementById('username_negative_feedback').style.display="block";
					document.getElementById('username_positive_feedback').style.display="none";
				}
		
}

function show_email_feedback(){
				if(document.getElementById('email_status').innerHTML=='Ok')
				{			
					document.getElementById('email_negative_feedback').style.display="none";
					document.getElementById('email_positive_feedback').style.display="block";
				}
			else
				{					
					document.getElementById('email_negative_feedback').style.display="block";
					document.getElementById('email_positive_feedback').style.display="none";
				}
		
}

function show_password1_feedback(){

				if(document.getElementById('password1_status').innerHTML=='OK')
				{			
					document.getElementById('password1_negative_feedback').style.display="none";
					document.getElementById('password1_positive_feedback').style.display="block";
				}
			else
				{					
					document.getElementById('password1_negative_feedback').style.display="block";
					document.getElementById('password1_positive_feedback').style.display="none";
				}
		
}

function show_password2_feedback(){
				if(document.getElementById('password2_status').innerHTML=='OK')
				{			
					document.getElementById('password2_negative_feedback').style.display="none";
					document.getElementById('password2_positive_feedback').style.display="block";
				}
			else
				{					
					document.getElementById('password2_negative_feedback').style.display="block";
					document.getElementById('password2_positive_feedback').style.display="none";
				}
		
}


var previous_email = '';
var in_ajax = 0;
function checkEmail() {
    email = $("#id_email").val();
    if (in_ajax != 1) {
        in_ajax = 1;
        $("#email_status").html("<img src='/images/icons/ajax_loading.gif'/>");
        $("#email_status").load('/check_email/', {email: email}, function() {in_ajax = 0;});
		window.setInterval("show_email_feedback()",25)
    }
    previous_email = email;
}

var previous_password1 = '';
var in_ajax = 0;
function checkPassword1() {
    password1 = $("#id_password1").val();
    if (in_ajax != 1) {
        in_ajax = 1;
        $("#password1_status").html("<img src='/images/icons/ajax_loading.gif'/>");
        $("#password1_status").load('/check_password1/', {password1: password1}, function() {in_ajax = 0;});
		window.setInterval("show_password1_feedback()",25)
    }
    previous_password1 = password1;
}

var previous_password2 = '';
var in_ajax = 0;
function checkPassword2() {
    password1 = $("#id_password1").val();
    password2 = $("#id_password2").val();
    if (in_ajax != 1) {
        in_ajax = 1;
        $("#password2_status").html("<img src='/images/icons/ajax_loading.gif'/>");
        $("#password2_status").load('/check_password2/', {password1: password1, password2: password2}, function() {in_ajax = 0;});
		window.setInterval("show_password2_feedback()",35)
    }
    previous_password2 = password2;
}

$(function() {
	$("#id_username").blur( function () { checkUsername(); } );
	$("#id_email").blur( function () { checkEmail(); } );
	$("#id_password1").blur( function () { checkPassword1(); } );
	$("#id_password2").blur( function () { checkPassword2(); } );
});

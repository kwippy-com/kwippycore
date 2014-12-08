<?php
include('openinviter.php');
$file=fopen($argv[1],"r");
while(!feof($file)) {
	$stuff = explode("|||",fgets($file));
	$scont[$stuff[1]]=$stuff[0];
}
fclose($file);
$inviter=new OpenInviter();
$inviter->startPlugin($argv[2]);
$internal=$inviter->getInternalError();
if ($internal) {
	echo "Error\nNot working";
} else {
	$message=array('subject'=>$inviter->settings['message_subject'],'body'=>$inviter->settings['message_body'],'attachment'=>"\n\rAttached message: \n\nrAll is good");
	$sendMessage=$inviter->sendMessage($argv[3],$message,$scont);
	$inviter->logout();
	if($sendMessage==-1) {
		echo "normal mailing";
	}
}
?>

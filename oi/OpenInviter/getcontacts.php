<?php
include('openinviter.php');
$inviter=new OpenInviter();
$inviter->startPlugin($argv[1]);
$internal=$inviter->getInternalError();
if($internal) {
	echo "Error\n$internal";
} elseif (!$inviter->login($argv[2],$argv[3])) {
	$internal=$inviter->getInternalError();
        echo "Error\nLogin failed. Please check the email and password you have provided and try again later";
} elseif (false===$contacts=$inviter->getMyContacts()) {
	echo "Error\nUnable to get contacts";
} else {
	echo $inviter->plugin->getSessionID()."\n";
	if ($inviter->showContacts()) {
		foreach ($contacts as $email=>$name) {
			echo "$name|||$email\n";
		}
	}
}
?>

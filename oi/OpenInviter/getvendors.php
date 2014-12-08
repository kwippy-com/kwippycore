<?php
include('openinviter.php');
$inviter=new OpenInviter();
$oi_services=$inviter->getPlugins();
foreach ($oi_services as $type=>$providers) {
	foreach ($providers as $provider=>$details) {
		echo $details['name']."|||$provider|||$type\n";
	}
}
?>

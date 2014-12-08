use Digest::SHA1  qw(sha1 sha1_hex sha1_base64);
open(USERCSV,">user.csv");
$init_str = "mailer";
$salt = "--Kwip--";
$count = 0;
$max = 200;
while($count<$max) {
$pass=sha1_base64("$salt$count");
print USERCSV "$init_str$count,kwippy,no-send,$pass=\n";
$count++;
}
close(USERCSV);

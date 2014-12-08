#!/usr/bin/perl


$title='mail test';
$to='dipankarsarkar@gmail.com';
$from= 'dipankar@kwippy.com';
$subject='Using Sendmail';

open(MAIL, "|/usr/sbin/sendmail -t");

## Mail Header
print MAIL "To: $to\n";
print MAIL "From: $from\n";
print MAIL "Subject: $subject\n\n";
## Mail Body
print MAIL "This is a test message from Yahoo! \n";

close(MAIL);

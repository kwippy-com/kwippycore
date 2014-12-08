#!/usr/bin/perl

use strict;
use DBI();
use Digest::SHA1  qw(sha1 sha1_hex sha1_base64);

my $dbh = DBI->connect("DBI:mysql:database=kwippy_staging1;host=localhost","kwippy_user1","helloworld69",{'RaiseError' => 1});

# Get the maximum count
my $sth=$dbh->prepare("select count(*) from kwippy_quip");
$sth->execute();
my $row=$sth->fetchrow_arrayref();
my $count_max = $$row[0];
$sth->finish();

# Get the lower limit
my $sth=$dbh->prepare("select count from kwippy_filtercount where fid=0");
$sth->execute();
my $row=$sth->fetchrow_arrayref();
my $count_min = $$row[0];
$sth->finish();

my $diff_count=$count_max - $count_min;

my $counter1=$count_min;
my $inc=100;

# $counter1 = 0;
# $diff_count = 10;
# $inc = 10;
print "$count_min $count_max\n";

while($counter1<$diff_count) {
	# Get the 100 quips
	my $sth=$dbh->prepare("select id,original,account_id from kwippy_quip order by id limit $counter1,$inc");
	$sth->execute();
	while(my $row=$sth->fetchrow_hashref()) {
		my $ai = $row->{'account_id'};
		my $id = $row->{'id'};
		my $txt = $row->{'original'};
		# got the data
		my $digest = sha1_base64($txt);
		# Check if hash there
		my $sth1=$dbh->prepare("select id,first_id from kwippy_rquip where hash='$digest' and acc_id=$ai");
		$sth1->execute();
		if( $sth1->rows == 0) {
			my $sth2=$dbh->prepare("select user_id from kwippy_account where id=$ai");
			$sth2->execute();
	                my $row2=$sth2->fetchrow_arrayref();
	                my $uid = $$row2[0];
	                $sth2->execute();
	                $sth2->finish();
			$dbh->do("insert into kwippy_rquip(hash,first_id,user_id,acc_id,count) values('$digest','$id','$uid','$ai','1')");
			$dbh->do("update kwippy_quip set repeat_id=$id where id=$id");
		} else {
			
			my $row1=$sth1->fetchrow_hashref();
			my $hid = $row1->{'id'};
			my $first_id = $row1->{'first_id'};
			
			$dbh->do("update kwippy_rquip set count=count+1 where id=$hid");
			$dbh->do("update kwippy_quip set repeat_id='$first_id' where id=$id");
		}
                $sth1->finish();
	}
	$sth->finish();
	$counter1+=$inc;
	print "*\n";
}
print "\n";
$dbh->do("update kwippy_filtercount set count=$count_max where fid=0");
$dbh->disconnect();

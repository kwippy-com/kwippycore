#!/usr/bin/perl

use strict;
use DBI();
use Digest::SHA1  qw(sha1 sha1_hex sha1_base64);

my $dbh = DBI->connect("DBI:mysql:database=kwippy_staging;host=localhost","kwippy_user","helloworld69",{'RaiseError' => 1});

# Get the maximum count
my $sth=$dbh->prepare("select max(id) from kwippy_quip");
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

# Get the number of rows to get 
my $sth=$dbh->prepare("select count(*) from kwippy_quip where id>$count_min");
$sth->execute();
my $row=$sth->fetchrow_arrayref();
my $diff_count = $$row[0];
$sth->finish();

my $counter1=0;
my $inc=100;

# print "$diff_count\n";

while($counter1<$diff_count) {
	# Get the 100 quips
	my $sth=$dbh->prepare("select id,original,account_id from kwippy_quip where id>$count_min order by id limit $counter1,$inc");
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
			# print "*\n";
			my $row1=$sth1->fetchrow_hashref();
			my $hid = $row1->{'id'};
			my $first_id = $row1->{'first_id'};
			
			$dbh->do("update kwippy_rquip set count=count+1 where id=$hid");
			$dbh->do("update kwippy_quip set repeat_id=$first_id where id=$id");
			$dbh->do("update comments_comment set object_id=$first_id where object_id=$id");
		}
                $sth1->finish();
	}
	$sth->finish();
	$counter1+=$inc;
#	print "*\n";
}
# print "\n";
$dbh->do("update kwippy_filtercount set count=$count_max where fid=0");
$dbh->disconnect();

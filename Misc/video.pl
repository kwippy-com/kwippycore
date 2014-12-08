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
my $sth=$dbh->prepare("select count from kwippy_filtercount where fid=1");
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
	my $sth=$dbh->prepare("select id,original from kwippy_quip order by id limit $counter1,$inc");
	$sth->execute();
	while(my $row=$sth->fetchrow_hashref()) {
		my $id = $row->{'id'};
		my $txt = $row->{'original'};
		# got the data
		if($txt =~ /http\:\/\/www\.youtube\.com\/watch\?v\=([a-zA-Z0-9_]*)/) {
			print "$1\n";
			my $embed='<br><object width="425" height="355"><param name="movie" value="http://www.youtube.com/v/'.$1.'"></param><param name="wmode" value="transparent"></param><embed src="http://www.youtube.com/v/'.$1.'&hl=en" type="application/x-shockwave-flash" wmode="transparent" width="425" height="355"></embed></object>';
			$dbh->do('update kwippy_quip set formated='.$dbh->quote($txt.$embed).' where id='.$id);
		}
	}
	$sth->finish();
	$counter1+=$inc;
	print "*\n";
}
print "\n";
$dbh->do("update kwippy_filtercount set count=$count_max where fid=1");
$dbh->disconnect();

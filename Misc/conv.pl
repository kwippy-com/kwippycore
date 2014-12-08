#!/usr/bin/perl

use strict;
use DBI();
use HTML::Entities;

my $dbh = DBI->connect("DBI:mysql:database=kwippy_staging1;host=localhost","kwippy_user1","helloworld69",{'RaiseError' => 1});

my $sth=$dbh->prepare("select count(*) from kwippy_quip");
$sth->execute();
my $row=$sth->fetchrow_arrayref();
print "Count is $$row[0]\n";
my $count1=$$row[0];
$sth->finish();
my $counter1=0;
while($counter1<$count1) {
	my $sth=$dbh->prepare("select id,original from kwippy_quip order by id limit $counter1,100");
	$sth->execute();
	while(my $row=$sth->fetchrow_hashref()) {
		my $id = $row->{'id'};
		my $txt = $row->{'original'};
		decode_entities($txt);
		$dbh->do("update kwippy_quip set formated=".$dbh->quote($txt)." where id=$id");
	}
	$sth->finish();
	$counter1+=100;
	print "*";
}
$dbh->disconnect();

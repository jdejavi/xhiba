#!/usr/bin/perl
use strict;
use File::Path qw(mkpath rmtree);


my $ipAddress        = '0.0.0.0';
my $domain = $ARGV[0];

open FILE, ">>", '/etc/hosts' or die $!;
		print FILE $ipAddress ."\t". $domain ."\n";
		close FILE;

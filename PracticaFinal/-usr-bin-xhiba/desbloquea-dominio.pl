#!/usr/bin/perl
use strict;
use File::Path qw(mkpath rmtree);

my $domain = $ARGV[0];

open IN, '< ', '/etc/hosts' or die $!;
		my @hostsFile = <IN>;
		close IN;
		    
		my @contents = grep(!/^0.0.0.0\t$domain/, @hostsFile);
		    
		open FILE, ">", '/etc/hosts' or die $!;
		print FILE @contents;
		close FILE;

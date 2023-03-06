#!/usr/bin/perl

use strict;
use warnings;

use CGI;
use DBI;
use CGI::Session();

my $q = CGI->new;


my $username   = $q->param('u');
my $password   = $q->param('p');

my $db = "xhiba";
my $host = "localhost";
my $user = "root";
my $pass = "password";

# Connect to the database
my $dbh = DBI->connect("DBI:MariaDB:database=$db;host=$host",
                       $user, $pass,
                       { RaiseError => 1, PrintError => 0 });

my $select = $dbh->prepare('SELECT username,password FROM users WHERE username = ?');
$select->execute($username);

if($select->rows() > 0){
	my @row = $select->fetchrow_array;
	my $user = $row[0];
	my $pass = $row[1];

	if($pass eq $password){
		my $session = new CGI::Session();
		$session->save_param($q);
		$session->expires("20h");
		$session->flush();
		#print $q->redirect("https://xhiba.com/~$user/");
		print $session->header(-location => "home.cgi");
		
	}else{
		print $q->redirect("https://xhiba.com/");
	}

}else{
	print $q->redirect("https://xhiba.com/");

}

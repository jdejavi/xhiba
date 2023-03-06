#!/usr/bin/perl

use strict;
use warnings;

use CGI;
use DBI;

my $q = CGI->new;


my $username   = $q->param('n');
my $email   = $q->param('u');
my $password   = $q->param('p');
my $name = $q->param('name');
my $surname = $q->param('surname');

my $db = "xhiba";
my $host = "localhost";
my $user = "root";
my $pass = "password";

if($username == undef || $email == undef || $password == undef){
	print $q->redirect("https://xhiba.com/");
}

# Connect to the database
my $dbh = DBI->connect("DBI:MariaDB:database=$db;host=$host",
                       $user, $pass,
                       { RaiseError => 1, PrintError => 0 });

my $select = $dbh->prepare('SELECT email FROM users WHERE email = ? or username = ?');
$select->execute($email,$username);

if($select->rows() == 0){
	# INSERT some data into 'foo' using placeholders
	my $stmt = $dbh->prepare('INSERT INTO users(username,email,password,register,name,surname,service_email,service_blog,service_web) VALUES (?,?, ?,?,?,?,1,1,0)');

	$stmt->execute($username,$email,$password,0,$name,$surname);

	# Disconnect from the database.
	$dbh->disconnect();
	print $q->redirect('https://xhiba.com/');
}else{
	print $q->redirect('https://xhiba.com/');

}



#!/usr/bin/perl

use strict;
use CGI;
use CGI::Session(); #Módulo para la sesion
use DBI;
#use CGI::Carp qw(fatalsToBrowser); #Muestra posibles errores en el navegador

#Creamos un objeto CGI
my $cgi = CGI->new();


#Creamos un objeto de sesión
my $session = new CGI::Session();

#Cargamos los datos de sesión
$session->load();

#recibir todos los parámetros de sesión
my @autenticar = $session->param;


if (@autenticar eq 0) #Si el usuario no ha iniciado sesión, es decir no hay parámetros de sesión guardados
{
	print $cgi->header();
	$cgi->start_html();
	print "Inicie sesión para acceder a esta página";
	$cgi->end_html();
}
elsif($session->is_expired) #Se la sesión ha expirado
{
	print $cgi->header();
	$cgi->start_html();
	print "Su sesión ha expirado";
	$cgi->end_html();
}
else #Todo ha ido correcto
{	
	
	my $db = "xhiba";
	my $host = "localhost";
	my $user = "root";
	my $pass = "password";
	my $username = $session->param("u");
	

	my $name   = $cgi->param('name');
	my $surname   = $cgi->param('surname');
	my $email	=$cgi->param('email');
	my $domain	= $cgi->param('dominio');
	# Connect to the database
	my $dbh = DBI->connect("DBI:MariaDB:database=$db;host=$host",
		               $user, $pass,
		               { RaiseError => 1, PrintError => 0 });

	my $select3 = $dbh->prepare('select * from users where username = ?');
	$select3->execute($username);

	my @datos = $select3->fetchrow_array();

	
	
	if($datos[10] ne "" ||$datos[10] != undef){
		my $select4 = $dbh->prepare('UPDATE domains set status = 2 WHERE user_id = ? and domain_name = ?');
		$select4->execute($datos[0],$datos[10]);
	}
	if($datos[9]==1){
		my $select = $dbh->prepare('insert into domains (domain_name,user,user_id,status) values (?,?,?,0)');
		$select->execute($domain,$username,$datos[0]);	
	}
	my $select2 = $dbh->prepare('UPDATE users set name = ?,surname = ?,email = ? ,domain = ? WHERE username = ?');
	$select2->execute($name,$surname,$email,$domain,$username);
	
	$dbh->disconnect();

	print $cgi->redirect("https://xhiba.com/cgi-bin/home.cgi");	

	
}

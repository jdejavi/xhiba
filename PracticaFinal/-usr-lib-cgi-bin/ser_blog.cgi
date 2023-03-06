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
	my $name = $session->param("u");
	# Connect to the database
	my $dbh = DBI->connect("DBI:MariaDB:database=$db;host=$host",
		               $user, $pass,
		               { RaiseError => 1, PrintError => 0 });

	my $prep = $dbh->prepare('SELECT service_blog FROM users WHERE username = ?');
	$prep->execute($name);
	
	my @row = $prep->fetchrow_array;

	if ($row[0] == 0){
		my $prep2 = $dbh->prepare('update users set service_blog = 1 WHERE username = ?');
		$prep2->execute($name);
	}else{
		my $prep2 = $dbh->prepare('update users set service_blog = 0 WHERE username = ?');
		$prep2->execute($name);

	}
	
	print $cgi->redirect("https://xhiba.com/cgi-bin/profile.cgi");
}

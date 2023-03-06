#!/usr/bin/perl

use strict;
use CGI;
use CGI::Session(); #Módulo para la sesion
use DBI;
use CGI::Carp qw(fatalsToBrowser); #Muestra posibles errores en el navegador
#use Linux::usermod;
#use CGI;
use Passwd::Unix;
#use File::Copy::Recursive qw(dircopy);
use MIME::Lite;

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
	$cgi->start_html();
	print '
		<!DOCTYPE html>
		<html lang="es">
		<head>
		  <meta charset="utf-8">
		  <title>Xhiba</title>
		  <link rel="stylesheet" href="/public/css/login.css">
		</head>

		<body>
		  <div class="login">
			<img class="shiba_logo" src="/public/images/Shiba.png">
			<h1>Cambio de contraseña</h1>
		    <form action="/cgi-bin/change-password.cgi" method="post">
			<input type="password" name="lPass" placeholder="Introduce tu contraseña anterior" required="required" />
			<input type="password" name="nPass" placeholder="Introduce la nueva contraseña" required="required" />
			<input type="password" name="nPassA" placeholder="Introduce de nuevo la nueva contraseña" required="required" />
		     
			<button type="submit" class="btn btn-primary btn-block btn-large">Change it.</button>
		    </form>
		</body>
		</html>
	';	
	$cgi->end_html();
}

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

	my $prep = $dbh->prepare('SELECT * FROM users WHERE username = ?');
	$prep->execute($name);
	
	my @datos = $prep->fetchrow_array;

	if ($datos[9] == 0){
		my $prep2 = $dbh->prepare('update users set service_web = 1 WHERE username = ?');
		$prep2->execute($name);

		my $select = $dbh->prepare('insert into domains (domain_name,user,user_id,status) values (?,?,?,0)');
		$select->execute($datos[10],$datos[1],$datos[0]);
	}else{
		my $prep2 = $dbh->prepare('update users set service_web = 0 WHERE username = ?');
		$prep2->execute($name);

		my $prep2 = $dbh->prepare('update domains set status = 2 WHERE user_id = ?');
		$prep2->execute($datos[0]);

	}
	
	print $cgi->redirect("https://xhiba.com/cgi-bin/profile.cgi");
}

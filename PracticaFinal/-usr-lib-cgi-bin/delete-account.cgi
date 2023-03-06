#!/usr/bin/perl

use strict;
use CGI;
use CGI::Session(); #Módulo para la sesion
use DBI;
use File::Path;


use Passwd::Unix;

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
	my $name = $session->param("u");
	my $db = "xhiba";
        my $host = "localhost";
        my $user = "root";
        my $pass = "password";
	my $dbh = DBI->connect("DBI:MariaDB:database=$db;host=$host",
                              $user, $pass,
                              { RaiseError => 1, PrintError => 0 });
        my $select = $dbh->prepare('SELECT username,password,email FROM users WHERE username = ?');
        $select->execute($name);
	
	if($select->rows()>0){
		my $passIntr = $cgi->param('pass');
		my @datos = $select->fetchrow_array;
		if($passIntr eq $datos[1]){
			#Procedemos a borrar la entrada de la base de datos
			
			my $actu = $dbh->prepare('UPDATE users SET register=3 where username =?');
			$actu->execute($name);
			my $prep2 = $dbh->prepare('UPDATE domains SET status=2 where user=?');
			$prep2->execute($name);
			$dbh->disconnect();
		
		print $cgi->redirect('https://xhiba.com/');		
		}
	}else{
		print $cgi->redirect('https://xhiba.com/cgi-bin/profile.cgi');
	}
}

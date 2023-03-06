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

#Creamos un objeto C
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
	my $select = $dbh->prepare('SELECT username,password FROM users WHERE username = ?');
	$select->execute($name);
	if($select->rows()>0){
		my @row = $select->fetchrow_array;
		my $oP = $cgi->param('lPass');
		#Si coincide la introducida con la anterior
		if($row[1] eq $oP){
			my $nP = $cgi->param('nPass');
			my $nPa = $cgi->param('nPassA');
			#Si coinciden las dos nuevas contraseñas
			if($nP eq $nPa){
				my $actu = $dbh->prepare('UPDATE users SET password=?,register=2 where username =?');
				$actu->execute($nP,$name);
				$dbh->disconnect();
				print $cgi->redirect('https://xhiba.com/cgi-bin/home.cgi')
			}#No coinciden ambas
			else{
			$dbh->disconnect();
			print $cgi->redirect('https://xhiba.com/cgi-bin/cambiaPDentro.cgi');
			}
		}#No coinciden las contraseñas antiguas
		else{
		$dbh->disconnect();
		print $cgi->redirect('https://xhiba.com/cgi-bin/cambiaPDentro.cgi');
		}
	}
}


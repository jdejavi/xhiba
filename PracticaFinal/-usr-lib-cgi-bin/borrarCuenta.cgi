#!/usr/bin/perl

use strict;
use CGI;
use CGI::Session(); #Módulo para la sesion
use DBI;



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
	$cgi->start_html();
	print '
                <html lang="es">
                <head>
                  <meta charset="utf-8">
                  <title>Xhiba</title>
                  <link rel="stylesheet" href="/public/css/login.css">
                </head>
                <body>
                <div class="login">
                <h1>¿Está seguro que desea eliminar su cuenta?</h1>
                    <form action="/cgi-bin/delete-account.cgi" method="post">
			 <input type="contr" name="pass" placeholder="Introduzca su contraseña "/>                        
                       <button type="sumbit" class="btn btn-primary btn-block btn-large">Comprobar</button>
                        </form>
                </div>
                </body>
                </html>
        ';

}

#!/usr/bin/perl

use strict;
use CGI;
use CGI::Session(); #Módulo para la sesion
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
	print'    <!DOCTYPE html>
        <html lang="es">
        <head>
          <meta charset="utf-8">
          <title>Xhiba</title>
          <link rel="stylesheet" href="/public/css/login.css">
        </head>
        <!--/public/images/-->
        <body>
          <div class="login">
            <img class="shiba_logo" src="/public/images/Shiba.png">
            <h1>Inicie Sesion para acceder</h1>
         </div>

        </body>
        </html>
    ';
	
#print "Inicie sesión para acceder a esta página";
	$cgi->end_html();
}
elsif($session->is_expired) #Se la sesión ha expirado
{
	print $cgi->header();
	$cgi->start_html();
	print'    <!DOCTYPE html>
        <html lang="es">
        <head>
          <meta charset="utf-8">
          <title>Xhiba</title>
          <link rel="stylesheet" href="/public/css/login.css">
        </head>
        <!--/public/images/-->
        <body>
          <div class="login">
            <img class="shiba_logo" src="/public/images/Shiba.png">
            <h1>Su sesion ha expirado</h1>
         </div>

        </body>
        </html>
    ';

	#print "Su sesión ha expirado";
	$cgi->end_html();
}
else #Todo ha ido correcto
{	
	#print $cgi->header();
	my $user = $session->param('u');
	$cgi->start_html();
	print '
		<html lang="es">
		<head>
		  <meta charset="utf-8">
		  <title>Xhiba</title>
		  <link rel="stylesheet" href="/public/css/home.css">
		</head>
		<body>
		    <div class="home">
			<div class="nav">
			    <a href="" class="logo">
				<img src="/public/images/Shiba.png"/>
			    </a>
			    <div class="user">
				    <a href="profile.cgi" class="profile" title="PERFIL">
					<img src="/public/images/perfil.png" title="PERFIL"/>
				    </a>
				    <a href="close-session.cgi" class="profile" title="CERRAR SESSION">
					<img src="/public/images/logout.png" title="PERFIL"/>
				    </a>
				    
			    </div>
			</div>
			<div class="content">
			    <div class="correo">
				<a href="/correo">
				    <img src="/public/images/email.png" title="EMAIL"/>
				</a>
			    </div>
			    <div class="blog">
				<a href="/wordpress/wp-login.php">
				    <img src="/public/images/blog.png" title="BLOG"/>
				</a>
			    </div>
			    <div class="web">
	';
	print qq(
				<a href="/~$user">
				    <img src="/public/images/website.png" title="WEB"/>
				</a>
			    </div>
			   
			</div>
		    </div>
		</body>
		</html>
	);	
	$cgi->end_html();
}




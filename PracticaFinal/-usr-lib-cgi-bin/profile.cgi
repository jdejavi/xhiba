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

#	print "Su sesión ha expirado";
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

	my $select = $dbh->prepare('SELECT * FROM users WHERE username = ?');
	$select->execute($name);	
	my @row = $select->fetchrow_array;

	$cgi->start_html();
	print '
		<!DOCTYPE html>
		<html lang="es">
		<head>
		  <meta charset="utf-8">
		  <title>Xhiba</title>
		  <link rel="stylesheet" href="/public/css/profile.css">
		</head>

		<body>
		  <div class="login">
			<img class="shiba_logo" src="/public/images/Shiba.png">
			<h1>Perfil</h1>
		    <form action="/cgi-bin/modify-profile.cgi" method="post">
	';
	print $cgi->textfield(
			-name => 'name',
			-placeholder => 'Nombre',
			-required => 'required',
			-value => "$row[5]"
			);

	print $cgi->textfield(
			-name => 'surname',
			-placeholder => 'Apellidos',
			-required => 'required',
			-value => "$row[6]"
			);
	print $cgi->textfield(
			-name => 'email',
			-placeholder => 'Correo',
			-required => 'required',
			-value => "$row[2]"
			);

	
	print $cgi->textfield(
			-name => 'dominio',
			-placeholder => 'Dominio',
			-value => "$row[10]"
			);   
	print '		<button type="submit" id="guardar-cambios" class="btn btn-primary btn-block btn-large">Guardar Cambios</button>
		    	</form>

			<form action="/cgi-bin/ser_email.cgi" method="post">';
				if ($row[7] == 0){
				print '		    <button type="submit" id="correo" class="btn btn-secondary btn-block btn-large" title="ALTA CORREO">Correo</button>';
				}else{
				print '		    <button type="submit" id="correo" class="btn btn-primary btn-block btn-large" title="BAJA CORREO">Correo</button>';
				}
	print '		</form>
			<form action="/cgi-bin/ser_blog.cgi" method="post">';
				if ($row[8] == 0){
				print '		    <button type="submit" id="blog" class="btn btn-secondary btn-block btn-large" title="ALTA BLOG">Blog</button>';
				}else{
				print '		    <button type="submit" id="blog" class="btn btn-primary btn-block btn-large" title="BAJA BLOG">Blog</button>';
				}

	print '		</form>
			<form action="/cgi-bin/ser_web.cgi" method="post">';
	
				if ($row[9] == 0){
					print '	    <button type="submit" id="web" class="btn btn-secondary btn-block btn-large" title="ALTA WEB">Web</button>';
				}else{
					print '	    <button type="submit" id="web" class="btn btn-primary btn-block btn-large" title="BAJA WEB">Web</button>';
				}
			
	print '	    </form>
		    <form action="/cgi-bin/cambiaPDentro.cgi" method="post">
		    	<button type="submit" id="cambia-contraseña" class="btn btn-danger btn-block btn-large">Cambiar constraseña</button>
		    </form>
		    <form action="/cgi-bin/eliminarCuenta.cgi" method="post">
			<button type="submit" id="elimina-usuario" class="btn btn-danger btn-block btn-large">Eliminar Usuario</button>
		    </form>
		</div>
		</body>
		</html>
	';	
	$cgi->end_html();
}

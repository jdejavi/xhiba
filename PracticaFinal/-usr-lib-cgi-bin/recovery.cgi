#!/usr/bin/perl

use DBI;
use strict;
use warnings;

use Linux::usermod;
use CGI;
use Passwd::Unix;
use File::Copy::Recursive qw(dircopy);
use MIME::Lite;
use HTTP::Request;
use LWP::UserAgent;

my $db = "xhiba";
my $host = "localhost";
my $user = "root";
my $pass = "password";

my $dB = DBI->connect("DBI:MariaDB:database=$db;host=$host",
                       $user, $pass,
                       { RaiseError => 1, PrintError => 0 });
#Recojo los datos del html proporcionados
my $q = CGI->new;


my $usuario   = $q->param('user');
my $email   = $q->param('mail');


my $prep = $dB->prepare('Select id,username,email from users where username = ? and email = ?') or die "Fallo en la preparacion";
$prep->execute($usuario,$email) or die;
if($prep->rows() > 0){
	#Numero random para validar el usuario, se le envia por correo
                my $topInf = 100000;
                my $topSup = 999999;
                my $number = $topInf + int(rand( $topSup - $topInf + 1 ));


                #Enviar correo de confirmacion
                my @datos = $prep->fetchrow_array();
                my $to = $datos[2];
                my $cc = 'root@xhiba.com';
                my $from = 'root@xhiba.com';
                my $subject = 'Codigo para cambio de contraseña';
                my $message = "Hola $datos[1] , introduce este codigo $number para seguir con el proceso de recuperacion de contraseña.";

                my $msg = MIME::Lite->new(
                                        From    => $from,
                                        To      => $to,
                                        Cc      => $cc,
                                        Subject => $subject,
                                        Data    => $message
                                        );
                $msg->send;
	

	#Me desconecto de la db
	$dB->disconnect();


	$q->start_html();
	print '
		<html lang="es">
		<head>
		  <meta charset="utf-8">
		  <title>Xhiba</title>
		  <link rel="stylesheet" href="/public/css/recovery.css">
		</head>
		<body>
		<div class="recovery">
		<h1>Comprobacion de numero</h1>
	';
	print $q->start_form(
			-name => 'formulario',
			-action => "/cgi-bin/comprueba.cgi",
			-method => 'POST'
			);
		print '<input type="numero" name="numero" placeholder="Introduce el numero enviado al correo" required="required"/>';
	print $q->hidden(
		-name => 'number',
		-value => "$number"
		);
	print $q->hidden(
		-name => 'id',
		-value => "$datos[0]"
		);

		print '	<button type="sumbit" class="btn btn-primary btn-block btn-large">Comprobar</button> 

		';
	print $q->end_form;

	print '	</div>
		</body>
		</html>
	';	
	$q->end_html();

	}
else{

	print $q->redirect("https://xhiba.com/");



}


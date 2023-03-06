#!/usr/bin/perl

use DBI;
use strict;
use warnings;

use Linux::usermod;
use CGI;
use Passwd::Unix;
use File::Copy::Recursive qw(dircopy);
use MIME::Lite;
#use Quota;

my $db = "xhiba";
my $host = "localhost";
my $user = "root";
my $pass = "password";
my $noreg =0;
my $dB = DBI->connect("DBI:MariaDB:database=$db;host=$host",
                       $user, $pass,
                       { RaiseError => 1, PrintError => 0 });
my $prep = $dB->prepare('Select * from users where register = ?') or die "Fallo en la preparacion";
$prep->execute($noreg) or die;


if($prep->rows() > 0){
        while(my @datos = $prep->fetchrow_array()){
		my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);

		$year += 1900;
		$mon++;

		my $fecha = "$year-$mday-$mon $hour:$min:$sec";
    	   #Crear usuario por cada row de datos
		my $gid = 1001;
		my $ruta = "/home/".$datos[1];
		my $us = Passwd::Unix->new();
		my $idUs = $us->unused_uid(1005);

		#Linux::usermod ->add($datos[1], $datos[3],$idUs,$gid," ",$ruta, "/bin/bash");
		my $pu = Passwd::Unix->new();
		my $pass = $pu->encpass($datos[3]);
		$pu->user("$datos[1]","$pass","$idUs","$gid","My user ","$ruta","/bin/bash");

		dircopy("/etc/skel/",$ruta);
		chown ($idUs, $gid, $ruta);
		chown($idUs,$gid,$ruta."/public_html");
		#chown($idUs,$gid,$ruta."/public_html/*");

		chmod (0700,$ruta);

		#Pone en la base de datos que esta registrado
		my $prep2 = $dB->prepare('Update users set register = 1 where id = ?');
		$prep2->execute($datos[0]) or die;
		

		#Registramos en wordpress al usuario
		my $db2 = "wordpress_db";
		my $user2 = "root";
		my $pass2 = "password";
		
		my $dB2 = DBI->connect("DBI:MariaDB:database=$db2;host=$host",
                       $user2, $pass2,
                       { RaiseError => 1, PrintError => 0 });

		$prep2 = $dB2->prepare('insert into wp_users values (?,?,MD5(?),?,?,"",?,"",0,?)');
		$prep2->execute($datos[0],$datos[1],$datos[3],$datos[1],$datos[2],$fecha,$datos[1]) or die;

		
		my $wp = "wp_user_level";
		$prep2 = $dB2->prepare('insert into wp_usermeta values (null,?,?,10)');
		$prep2->execute($datos[0],$wp) or die;

		$wp = "wp_capabilities";
		my $permisos = 'a:1:{s:6:"author";b:1;}';
		$prep2 = $dB2->prepare('insert into wp_usermeta values (null,?,?,? )');
		$prep2->execute($datos[0],$wp,$permisos) or die;
		$dB2->disconnect();

		#Enviar correo de confirmacion
		my $to = $datos[2];
		my $cc = 'root@xhiba.com';
		my $from = 'root@xhiba.com';
		my $subject = 'Bienvenido a XHIBA';
		my $message = "Hola $datos[1] , su cuenta en Xhiba ya se encuentra disponible";
		
		my $msg = MIME::Lite->new(
					From	=> $from,
					To	=> $to,
					Cc	=> $cc,
					Subject	=> $subject,
					Data	=> $message
					);
		$msg->send;
		my $output2 = `/usr/bin/xhiba/cuotaUp $datos[1] $datos[3]`;
		print $output2;
	}
	$dB->disconnect();
	
}


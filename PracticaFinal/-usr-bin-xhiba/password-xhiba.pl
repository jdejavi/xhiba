#!/usr/bin/perl

use DBI;
use strict;
use warnings;

use Linux::usermod;
use CGI;
use Passwd::Unix;
use MIME::Lite;

		my $db = "xhiba";
		my $host = "localhost";
		my $user = "root";
		my $pass = "password";
		my $dB = DBI->connect("DBI:MariaDB:database=$db;host=$host",
                       $user, $pass,
                       { RaiseError => 1, PrintError => 0 });



		my $prep2 = $dB->prepare('select * from users where register = 2');
		$prep2->execute() or die;

if($prep2->rows() > 0){
        while(my @rows = $prep2->fetchrow_array()){


		#Registramos en wordpress al usuario
		my $db2 = "wordpress_db";
		my $user2 = "root";
		my $pass2 = "password";
		
		my $dB2 = DBI->connect("DBI:MariaDB:database=$db2;host=$host",
                       $user2, $pass2,
                       { RaiseError => 1, PrintError => 0 });

		my $prep3 = $dB2->prepare('Update wp_users set user_pass=MD5(?) where ID = ?');
		$prep3->execute($rows[3],$rows[0]) or die;
		

 		my $to = $rows[2];
                my $cc = 'root@xhiba.com';
                my $from = 'root@xhiba.com';
                my $subject = 'Cambio de contraseña';
                my $message = "Tu nueva contraseña nueva es $rows[3], puedes cambiarla iniciando sesion en tu cuenta"; 

                my $msg = MIME::Lite->new(
                                        From    => $from,
                                        To      => $to,
                                        Cc      => $cc,
                                        Subject => $subject,
                                        Data    => $message
                                        );
                $msg->send;


		#Le cambio la contraseña al usuario del ordenador

		my $pu = Passwd::Unix->new();
		my $pass = $pu->encpass($rows[3]);
		my @usuario = $pu->user($rows[1]);

		$pu->user("$rows[1]" ,"$pass", "$usuario[1]","$usuario[2]","$usuario[3]","$usuario[4]","$usuario[5]");

		#Pone en la base de datos que esta registrado
		my $prep2 = $dB->prepare('Update users set register = 1 where id = ?');
		$prep2->execute($rows[0]) or die;

	}
}




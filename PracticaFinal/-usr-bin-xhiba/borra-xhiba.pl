#!/usr/bin/perl

use DBI;
use strict;
use warnings;

use Linux::usermod;
use CGI;
use Passwd::Unix;
use File::Copy::Recursive qw(dircopy);
use File::Path;
use MIME::Lite;
#use Quota;

my $db = "xhiba";
my $host = "localhost";
my $user = "root";
my $pass = "password";
my $dB = DBI->connect("DBI:MariaDB:database=$db;host=$host",
                       $user, $pass,
                       { RaiseError => 1, PrintError => 0 });
my $prep = $dB->prepare('Select * from users where register = 3') or die "Fallo en la preparacion";
$prep->execute() or die;

if($prep->rows() > 0){
        while(my @datos = $prep->fetchrow_array()){

		my $select2 = $dB->prepare('DELETE FROM users WHERE username = ?');
		$select2->execute($datos[1]);
		#Procedemos a borrar el usuario por completo
		my $directorio = "/home/".$datos[1];
		print $directorio;
		my $output2 = `/usr/bin/xhiba/cuotaDown $datos[1]`;
                print $output2;
		Passwd::Unix->del($datos[1]);
		rmtree($directorio,1,1);
		#Borramos al usuario de wordpress
		my $db2 = "wordpress_db";
		my $user2 = "root";
		my $pass2 = "password";
		
		my $dB2 = DBI->connect("DBI:MariaDB:database=$db2;host=$host",
                       $user2, $pass2,
                       { RaiseError => 1, PrintError => 0 });

		$select2 = $dB2->prepare('DELETE FROM wp_users WHERE ID = ?');
		$select2->execute($datos[0]);

		$select2 = $dB2->prepare('DELETE FROM wp_usermeta WHERE user_id = ?');
		$select2->execute($datos[0]);

		
		#Usuario borrado, enviamos correo
		my $to = $datos[2];
                my $cc = 'root@xhiba.com';
                my $from = 'root@xhiba.com';
                my $subject = 'Baja de cuenta';
                my $message = "Le informamos desde XHIBA que su cuenta ha sido dada de baja."; 

                my $msg = MIME::Lite->new(
                                        From    => $from,
                                        To      => $to,
                                        Cc      => $cc,
                                        Subject => $subject,
                                        Data    => $message
                                        );
                $msg->send;
	}
	$dB->disconnect();
}

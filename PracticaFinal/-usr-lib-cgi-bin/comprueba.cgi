#!/usr/bin/perl

use DBI;
use strict;
use warnings;

use Linux::usermod;
use CGI;
use Passwd::Unix;
use File::Copy::Recursive qw(dircopy);
use MIME::Lite;
use Data::Rand;


#Compruebo el numero que me ha pasado el form anterior
my $q = CGI->new;
my $numerito = $q->param('number');
my $num = $q->param('numero');
my $id = $q->param('id');

#print $q->header();

if($numerito eq $num){
		my $topInf = 100000;
                my $topSup = 999999;
                my $passN = $topInf + int(rand( $topSup - $topInf + 1 ));

		my $db = "xhiba";
		my $host = "localhost";
		my $user = "root";
		my $pass = "password";
		my $dB = DBI->connect("DBI:MariaDB:database=$db;host=$host",
                       $user, $pass,
                       { RaiseError => 1, PrintError => 0 });
	
		my $prep2 = $dB->prepare('select * from users where id = ?');
		my $select = $prep2->execute($id) or die;

		my @rows = $prep2->fetchrow_array;

		
                my $to = $rows[2];
                my $cc = 'root@xhiba.com';
                my $from = 'root@xhiba.com';
                my $subject = 'Cambio de contraseña';
                my $message = "Tu nueva contraseña nueva es $passN, puedes cambiarla iniciando sesion en tu cuenta"; 

                my $msg = MIME::Lite->new(
                                        From    => $from,
                                        To      => $to,
                                        Cc      => $cc,
                                        Subject => $subject,
                                        Data    => $message
                                        );
                $msg->send;
		#Cambio la contraseña en la BD
		

		$prep2 = $dB->prepare('Update users set password = ? where id = ?');
		$prep2->execute($passN,$id) or die;
		$dB->disconnect();
		
		#Le cambio la contraseña al usuario del ordenador
		#my $pu = Passwd::Unix->new();
		#$pu->passwd($rows[1],$passN);
		my $pu = Passwd::Unix->new();
		my $pass = $pu->encpass($passN);
		my @usuario = $pu->user($rows[1]);
		$pu->user("$rows[1]" ,"$pass", "$usuario[1]","$usuario[2]","$usuario[3]","$usuario[4]","$usuario[5]");
		print $q->redirect('https://xhiba.com/');
}

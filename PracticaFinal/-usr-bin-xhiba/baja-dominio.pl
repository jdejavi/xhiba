#!/usr/bin/perl -w
use strict;
use File::Path qw(mkpath rmtree);
use Getopt::Long;
use DBI;
 
my $db = "xhiba";
my $host = "localhost";
my $user = "root";
my $pass = "password";
my $dB = DBI->connect("DBI:MariaDB:database=$db;host=$host",
                       $user, $pass,
                       { RaiseError => 1, PrintError => 0 });
my $prep = $dB->prepare('Select * from domains where status = 2') or die "Fallo en la preparacion";
$prep->execute() or die;

if($prep->rows() > 0){
        while(my @datos = $prep->fetchrow_array()){

		


		my $ipAddress        = '127.0.1.1';
		my $apacheDir	     = '/etc/apache2/sites-available';
		my $docRoot          = '/home/'.$datos[2].'/public_html';
		my $logsDir          = 'logs';
		my $domain = $datos[1];

		my $apacheFile = $apacheDir . '/' . $domain .'.conf';
		my $archivo = $domain .'.conf';

		open IN, '< ', '/etc/hosts' or die $!;
		my @hostsFile = <IN>;
		close IN;
		    
		my @contents = grep(!/^127.0.1.1\t$domain/, @hostsFile);
		    
		open FILE, ">", '/etc/hosts' or die $!;
		print FILE @contents;
		close FILE;
		    
		my $output = `/usr/sbin/a2dissite $archivo`;
		print $output;
		    

		unlink($apacheFile);

		my $output2 = `/etc/init.d/apache2 restart`;
		print $output2; 

		my $select2 = $dB->prepare('DELETE FROM domains WHERE user_id = ?');
		$select2->execute($datos[3]);

	}
}

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
my $prep = $dB->prepare('Select * from domains where status = 0') or die "Fallo en la preparacion";
$prep->execute() or die;

if($prep->rows() > 0){
        while(my @datos = $prep->fetchrow_array()){

		my $select4 = $dB->prepare('UPDATE domains set status = 1 WHERE user_id = ?');
		$select4->execute($datos[3]);

		my $ipAddress        = '127.0.1.1';
		my $apacheDir	     = '/etc/apache2/sites-available';
		my $docRoot          = '/home/'.$datos[2].'/public_html';
		my $logsDir          = 'logs';
		my $domain = $datos[1];

		my $apacheFile = $apacheDir . '/' . $domain .'.conf';
		my $archivo = $domain .'.conf';
		 
		    my $vhostContent = << "EOF";
			<VirtualHost *:80>
			    ServerName $domain
			    DocumentRoot $docRoot
			    <Directory $docRoot>
				Options Indexes FollowSymLinks
				AllowOverride All
				Order allow,deny
				Allow from all
			    </Directory>
		 	</VirtualHost>
		 
EOF

		open FILE,">",$apacheFile or die $!;
		print FILE $vhostContent;
		close FILE;
		 
		open FILE, ">>", '/etc/hosts' or die $!;
		print FILE $ipAddress ."\t". $domain ."\n";
		close FILE;

		my $output = `/usr/sbin/a2ensite $archivo`;
		print $output;
		 
		my $output2 = `/etc/init.d/apache2 restart`;
		print $output2; 

		
	}
}


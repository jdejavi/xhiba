#!/usr/bin/perl

use Archive::Zip;

my $zip = Archive::Zip->new();

my @files=</home/*>;
	foreach my $a (@files){
			my $ruta = '/home/'.$a;
			$zip->addTree($ruta,$a);
			unless ( $zip->writeToFileNamed($a.'.zip') == AZ_OK ) {
			        die 'write error';
		        }
}
    @files=</var/www/*>;
	foreach my $a (@files){
                        $ruta = '/var/www/'.$a;
                        $zip->addTree($ruta,$a);
                        unless ( $zip->writeToFileNamed($a.'.zip') == AZ_OK ) {
                                die 'write error';
                        }
        }
@files=</var/lib/mysql/*>;
       	foreach my $a (@files){
                        $ruta = '/var/lib/mysql/'.$a;
                        $zip->addTree($ruta,$a);
                        unless ( $zip->writeToFileNamed($a.'.zip') == AZ_OK ) {
                                die 'write error';
                        }
        }
	@files=</var/log/monitorizacion/*>;
        foreach my $a (@files){
                        $ruta = '/var/log/monitorizacion/'.$a;
                        $zip->addTree($ruta,'logs');
                        unless ( $zip->writeToFileNamed($a.'.zip') == AZ_OK ) {
                                die 'write error';
                        }
        }


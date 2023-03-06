#!/usr/bin/perl

use strict;
use CGI;
use CGI::Session();

my $session = new CGI::Session();
my $q = CGI->new();

$session->load();
$session->delete();

print $q->redirect("https://xhiba.com/");

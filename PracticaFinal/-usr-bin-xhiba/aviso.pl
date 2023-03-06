#!/usr/bin/perl
use warnings;
use strict;
use MIME::Lite;
#Enviar correo de confirmacion
                my $to = 'jdejavi5@gmail.com';
                my $cc = 'root@xhiba.com';
                my $from = 'root@xhiba.com';
                my $subject = 'Inicio sesion administrador';
                my $message = "Hola, se ha iniciado sesión con root. Si no ha sido usted, arranque los cables del ordenador :)";

                my $msg = MIME::Lite->new(
                                        From    => $from,
                                        To      => $to,
                                        Cc      => $cc,
                                        Subject => $subject,
                                        Data    => $message
                                        );
                $msg->send;

#!/bin/sh

umount /home/$1/public_html
umount /home/$1
ejabberdctl unregister $1 xhiba.com

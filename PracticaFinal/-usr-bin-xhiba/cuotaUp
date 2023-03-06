#!/bin/bash
#chown -R $1:usuarios /home/$1

if [ -f /var/parti/tamanio_usu$1.ext2 ];
then
mount -o loop,rw,usrquota,grpquota -t ext2 /var/parti/tamanio_usu$1.ext2 /home/$1/
else
dd if=/dev/zero of=/var/parti/tamanio_usu$1.ext2 bs=80M count=1
mkfs.ext2 /var/parti/tamanio_usu$1.ext2
mount -o loop,rw,usrquota,grpquota -t ext2 /var/parti/tamanio_usu$1.ext2 /home/$1/
fi

if [ -f /var/parti/tamanio_publ$1.ext2 ];
then
mount -o loop,rw,usrquota,grpquota -t ext2 /var/parti/tamanio_publ$1.ext2 /home/$1/public_html
else
dd if=/dev/zero of=/var/parti/tamanio_publ$1.ext2 bs=5M count=1
mkfs.ext2 /var/parti/tamanio_publ$1.ext2
if [ -d /home/$1/public_html ];
then
#cp /etc/skel/public_html /home/$1

	if [ -f /home/$1/lost+found ];
	then
		mv /home/$1/lost+found /home/$1/.lost+found
	fi
	mount -o loop,rw,usrquota,grpquota -t ext2 /var/parti/tamanio_publ$1.ext2 /home/$1/public_html
else
cp /etc/skel/public_html /home/$1
	if [ -f /home/$1/lost+found ];
        then
                mv /home/$1/lost+found /home/$1/.lost+found
       	fi
mount -o loop,rw,usrquota,grpquota -t ext2 /var/parti/tamanio_publ$1.ext2 /home/$1/public_html
fi
fi
chown -R $1:usuarios /home/$1
chown -R $1:usuarios /home/$1/public_html
ejabberdctl register $1 xhiba.com $2

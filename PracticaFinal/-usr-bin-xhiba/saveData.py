#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dropbox
import os
from datetime import datetime

class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to)

def main():
    access_token = 'GodYWRMs05sAAAAAAAAAASdaJAsk3Hvu6w5PpkuIA-zwaMNVoVhhME7hKPnR1UoW'
    transferData = TransferData(access_token)
    fileDir = r"/home"
    fileDir1 = r"/var/www"
    fileDir2 = r"/var/lib/mysql"
    fileDir3 = r"/var/log/monitorizacion"
    fileExtens = r".zip"

    now = datetime.now()
    cadena1 = str(str(now.day)+'-'+str(now.month)+'-'+str(now.year))	

    archivos=[archivo for archivo in os.listdir(fileDir) if archivo.endswith(fileExtens)]
    for x in range(0,len(archivos)):
		
        file_from = '/home/'+archivos[x]
 	file_to = str('/'+cadena1+'HOME/'+archivos[x])  # The full path to upload the file to, including the file name
	#print archivos[x]
	transferData.upload_file(file_from, file_to)
	os.remove(os.path.join("/home",archivos[x]))
		

   
    cadena2 = str(str(now.day)+'-'+str(now.month)+'-'+str(now.year))

    archivos=[archivo for archivo in os.listdir(fileDir1) if archivo.endswith(fileExtens)]
    for x in range(0,len(archivos)):
		
        file_from = '/var/www/'+archivos[x]
 	file_to = str('/'+cadena2+'VARWWW/'+archivos[x])  # The full path to upload the file to, including the file name
	#print archivos[x]
	transferData.upload_file(file_from, file_to)
	os.remove(os.path.join("/var/www",archivos[x]))


    cadena3 = str(str(now.day)+'-'+str(now.month)+'-'+str(now.year))	

    archivos=[archivo for archivo in os.listdir(fileDir2) if archivo.endswith(fileExtens)]
    for x in range(0,len(archivos)):
		
        file_from = '/var/lib/mysql/'+archivos[x]
 	file_to = str('/'+cadena3+'MYSQL/'+archivos[x])  # The full path to upload the file to, including the file name
	#print archivos[x]
	transferData.upload_file(file_from, file_to)
	os.remove(os.path.join("/var/lib/mysql",archivos[x]))
    cadena4 = str(str(now.day)+'-'+str(now.month)+'-'+str(now.year))    

    archivos=[archivo for archivo in os.listdir(fileDir3) if archivo.endswith(fileExtens)]
    for x in range(0,len(archivos)):

        file_from = '/var/log/monitorizacion/'+archivos[x]
        file_to = str('/'+cadena4+'LOG/'+archivos[x])  # The full path to upload the file to, including the file name
        #print archivos[x]
        transferData.upload_file(file_from, file_to)
        os.remove(os.path.join("/var/log/monitorizacion",archivos[x]))
    # API v2
    
if __name__ == '__main__':
    main()


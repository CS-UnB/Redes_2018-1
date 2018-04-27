#!/usr/bin/python3           # This is client.py file

import socket

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()                           
print(host)
port = 80

# connection to hostname on the port.
s.connect((host, port))                               

# Receive no more than 1024 bytes
service = input("Would you like to...?:\n\tUpload (file)\t\tDownload (file)\n")         

#MENU:
#if service == 'upload':
#		s.send('downstream.file')
#elif service == 'download':
#		s.recv(1024)                            
#else:
while True:	
	msg = s.recv(1024)
	if not msg:
		break

s.close()
print (msg.decode('ascii'))
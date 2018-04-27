#!/usr/bin/python3           # This is server.py file
import socket                                         

# create a socket object
serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()                           
print(host)
port = 80  

# bind to the port
serversocket.bind((host, port))                                  

# opens file to write data to
#f = open('torcv.txt', 'wb')

# queue up to 5 requests
serversocket.listen(5)  

while True:
   try:
      # establish a connection
      clientsocket,addr = serversocket.accept()      
      print("Got a connection from %s" % str(addr))
   #   msg = clientsocket.recv(1024)                                         	
   #   print(msg)

      print("Receiving \n")

      #f.close()
      print("Done receiving\n")
       
      msg = 'Thank you for connecting'+ "\r\n"
      clientsocket.send(msg.encode('ascii'))
      clientsocket.close()
   except KeyboardInterrupt:
      pass
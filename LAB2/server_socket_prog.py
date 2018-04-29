#!/usr/bin/python3           # This is server.py file
# CONTINUE from testing GET and developing POST objects
import socket 
from threading import *
import os.path  

class client_thread(Thread):

   def __init__(self, socket, address):
      Thread.__init__(self)
      self.sock = socket
      self.addr = address
      self.start()

class MyServer:
## START __METHODS__ #########################################################
   def __init__(self, sock=None):
      if sock is None:
         self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      else:
         self.sock = sock

   def bind_to(self, port=80, host=None):
      if host is None:
         host = socket.gethostname()
      self.sock.bind((host, port))
      print ('Server ' + host + ' binded to port ' + str(port) + '\r\n')

   def listen_to(self, clients=3):
      self.sock.listen(clients)

   def accept_inbound_connection(self):
      (client_socket,addr) = self.sock.accept()      
      client = client_thread(client_socket, addr)
      print ("Got a connection from %s" % str(addr))
      return client

   def respond(self, client, msg=None):
      if msg is None:
         msg = 'Thank you for connecting\r\n'
      client.sock.send(msg.encode('UTF-8'))

   def handle_get(self, client, target):
      if os.path.isfile(target):
         print(target +' object found\n')
         self.respond(client, str('204\r\nRequested Object '+ target +' found\r\n'))
         self.send_object(client, target)
      else:
         print (target +' NOT FOUND')
         self.respond(client, str('404\r\nRequested Object '+ target +' not found\r\n'))

   def handle_post(self, client, target):
      #self.respond(client, str('104\r\nReady to receive object\r\n'))
      self.receive_object(client, target)

   def receive_request(self, client):
      request = client.sock.recv(1024).decode()
      method, host, target, port = request.split("\r\n", 3)
      # cleaning meta-data
      method = method[:3]
      print (method)
      host = host[5:] 
      target = target[7:]
      port = port[5:]
      
      # resolving request 
      #if host != socket.gethostname():
      #   print ('Requested host '+ host +' does not match localhost '+ socket.gethostname() +'\n')
      #   self.respond(client, '400\r\nIncorrect HOST reached!\r\n')
      #else:
      if method == 'GET':
         print ('Object '+ target +' requested by client '+ str(client.addr) +'\n')
         self.handle_get(client, target)
      elif method == 'POS':
         print ('Object '+ target +' posted by client '+ str(client.addr) +'\n')
         self.handle_post(client, target)


   def receive_object(self, client, file_name):
      with open(str('./server_'+ file_name), 'wb') as f:
         data = client.sock.recv(1024)
         while data:
            print ('\nReceiving object...\n')
            f.write(data)
            data = client.sock.recv(1024)
         client.sock.close()
         print ('Done receiving object.\n')

   def send_object(self, client, file_name):
      print ('Sending object\n')
      with open(file_name, 'rb') as f:
         client.sock.sendfile(f, 0)
      print ('Done sending object\n\n')
      client.sock.close()
## END __METHODS__ ###########################################################

def Main():
   server = MyServer()
   server.bind_to()           # binds to localhost if none specified
   server.listen_to(3)
   for i in range(5):
         # receive connection from clients
         client_thread = server.accept_inbound_connection()
         server.receive_request(client_thread)
         # close client socket ?
   server.sock.close()

if __name__ == '__main__':
   Main()
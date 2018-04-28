#!/usr/bin/python3           # This is server.py file
import socket 
from threading import *
import sys       

class client_thread(Thread):

   def __init__(self, socket, address):
      Thread.__init__(self)
      self.sock = socket
      self.addr = address
      self.start()

class MyServer:

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

   def close_socket(self):
      self.sock.close()

   def respond(self, client, msg=None):
      if msg is None:
         msg = 'Thank you for connecting\r\n'
      client.sock.send(msg.encode('UTF-8'))

   def receive(self):
      response = ''
      while (True):
          recv = self.sock.recv(1024)
          if not recv:
              break
          response += recv.decode()
      print (response)

   def receive_file(self, client, file_name='name.type'):
      f = open(file_name, 'wb')
      while (True):
         l = client.sock.recv(1024)
         while (l):
            f.write(l)
            l = client.sock.recv(1024)
      f.close()

def Main():
   server = MyServer()
   server.bind_to()           # binds to localhost if none specified
   server.listen_to(3)
   for i in range(5):
         # receive connection from clients
         client = server.accept_inbound_connection()
         #server.respond(client, )
         data = client.sock.recv(1024).decode()
         print (data)
         client.sock.close()
   server.sock.close()

if __name__ == '__main__':
   Main()
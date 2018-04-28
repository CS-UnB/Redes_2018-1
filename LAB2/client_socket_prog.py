import socket

class MyClient:

	def __init__(self, sock=None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock

	def connect_to_host(self, host=socket.gethostname(), port=80):
		self.sock.connect((host, port))

	def get(self, host, port=80):
		request_header = 'GET / HTTP/1.0\r\nHost:' + host + '\r\nPort:' + str(port) + '\r\n\r\n'
		self.sock.send(request_header.encode('UTF-8'))

	def receive(self):
		response = ''
		while True:
		    recv = self.sock.recv(1024)
		    if not recv:
		        break
		    response += recv.decode()
		print (response)
	
	def send_file(self, file_name='name.type'):
		f = open(file_name, 'rb')
		l = f.read(1024)
		while(l):
			self.sock.send(l)
			l = f.read(1024)
		f.close()
	def receive_file(self, client, file_name='name.type'):
      f = open(file_name, 'wb')
      while (True):
         l = client.sock.recv(1024)
         while (l):
            f.write(l)
            l = client.sock.recv(1024)
      f.close()
      
	def close(self):
		self.sock.close()

def Main():
	client_socket = MyClient()
	client_socket.connect_to_host()
	#client_socket.receive()
	client_socket.get(socket.gethostname(), )

if __name__ == '__main__':
	Main()

# CONTINUE from testing GET and developing POST objects
import socket

class MyClient:
## START __METHODS__ #########################################################
	def __init__(self, sock=None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock

	def connect_to_host(self, host=socket.gethostname(), port=80):
		self.host = host
		self.sock.connect((host, port))

	def wait_reply(self, object):
		response = self.sock.recv(1024).decode()

		if response[:3] == '400':
			print ('Incorrect host reached. Please, retry.\n')
		elif response[:3] == '404':
			print ('File not found in host\n')
		elif response[:3] == '204':
			print ('Object found. Receiving it...\n')
			self.receive_object(object)

	def get(self, host, target, port=80):
		request_header = 'GET / HTTP/1.0\r\nHost:'+ host +'\r\nTarget:'+ target +'\r\nPort:'+ str(port) +'\r\n\r\n'
		self.sock.send(request_header.encode('UTF-8'))
		self.sock.shutdown(socket.SHUT_WR) # signals it has finished sending
		self.wait_reply(target)
		#self.sock.close()
		
	def send_file(self, file_name):
		print ('Sending object\n')
		with open(file_name, 'rb') as f:
			self.sock.sendfile(f, 0)
		print ('Done sending object\n\n')
		self.sock.close()

	def receive_object(self, file_name):
		with open(str('./client_'+ file_name[2:]), 'wb') as f:
			data = self.sock.recv(1024)
			while data:
				print ('\nReceiving object...\n')
				f.write(data)
				data = self.sock.recv(1024)
			self.sock.close()
			print ('Done receiving object.\n')

## END __METHODS__ ############################################################

def Main():
	client = MyClient()
	client.connect_to_host()
	client.get(str(client.host), './txt1.txt', )

if __name__ == '__main__':
	Main()

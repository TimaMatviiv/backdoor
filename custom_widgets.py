from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



class ClientItem(QListWidgetItem):
	def __init__(self, connection, address):
		super().__init__()
		
		self.connection = connection
		self.address = address

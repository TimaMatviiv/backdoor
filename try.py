import json
import base64

img = open("Phishing.pptx", "rb").read()
print(img[0:10])

b_img = base64.encodebytes(img).decode('utf-8')
print(json.dumps(b_img)[0:10])


l_img = base64.b64decode(b_img)
print(l_img[0:10])


with open("bla-bla.pptx", "wb") as new_img:
	new_img.write(l_img)



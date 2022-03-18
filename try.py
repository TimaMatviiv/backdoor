import PyInstaller.__main__
import os
    
PyInstaller.__main__.run([  
     'name-%s%' % 'server.py',
     '-w',
     os.path.join('/path/to/your/script/', 'server.py')                                       
])




# import json
# import base64

# img = open("Phishing.pptx", "r
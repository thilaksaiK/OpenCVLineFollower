#This code shows how to acquire frames using IpWebCam

import urllib.request
import cv2
import numpy as np

# The Url displayed on IPWebCam app
url = 'http://192.168.43.1:8080/shot.jpg'


while True:
    # Use urllib to get the image from the IP camera
    imgResp = urllib.request.urlopen(url)

    # Numpy to convert into a array
    imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)

    # Finally decode the array to OpenCV usable format ;)
    image = cv2.imdecode(imgNp, -1)
    
    # Display the image Using imshow
    cv2.imshow('IPWebcam', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

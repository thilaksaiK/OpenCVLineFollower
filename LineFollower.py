import urllib.request
import cv2
import numpy as np
import time
import serial

ser = serial.Serial('com10', 9600, timeout=.1)
time.sleep(1)

url = 'http://192.168.43.1:8080/shot.jpg'
a = 0

seconds = time.time()
x_setPoint = 120
angle_Limit = 15
Error_Limit = 30

x_last = 72
y_last = 88

kp = 3
ap = 2
maxSteer = 72*kp + 89*ap
kernel = np.ones((3, 3), np.uint8)

imgResp = urllib.request.urlopen(url)                           # Use urllib to get the image from the IP camera
imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)     # Numpy to convert into a array
previousImage = cv2.imdecode(imgNp, -1)                                 # Finally decode the array to OpenCV usable format

while True :

    imgResp = urllib.request.urlopen(url)                           # Use urllib to get the image from the IP camera
    imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)     # Numpy to convert into a array
    image = cv2.imdecode(imgNp, -1)                                 # Finally decode the array to OpenCV usable format
    b, g, r = cv2.split(image-previousImage)
    if cv2.countNonZero(b) > 1000:
        previousImage = image
        Blackline = cv2.inRange(image, (0, 0, 0), (75, 75, 75))
        Blackline = cv2.erode(Blackline, kernel, iterations=1)
        Blackline = cv2.dilate(Blackline, kernel, iterations=2)
        contours_blk, hierarchy_blk = cv2.findContours(Blackline.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contours_blk_len = len(contours_blk)
        if contours_blk_len > 0:
            if contours_blk_len == 1:
                blackbox = cv2.minAreaRect(contours_blk[0])
            else:
                canditates = []
                off_bottom = 0
                for con_num in range(contours_blk_len):
                    blackbox = cv2.minAreaRect(contours_blk[con_num])
                    (x_min, y_min), (w_min, h_min), ang = blackbox
                    box = cv2.boxPoints(blackbox)
                    (x_box, y_box) = box[0]
                    if y_box > 358:
                        off_bottom += 1
                    canditates.append((y_box, con_num, x_min, y_min))
                canditates = sorted(canditates)
                if off_bottom > 1:
                    canditates_off_bottom = []
                    for con_num in range((contours_blk_len - off_bottom), contours_blk_len):
                        (y_highest, con_highest, x_min, y_min) = canditates[con_num]
                        total_distance = (abs(x_min - x_last) ** 2 + abs(y_min - y_last) ** 2) ** 0.5
                        canditates_off_bottom.append((total_distance, con_highest))
                    canditates_off_bottom = sorted(canditates_off_bottom)
                    (total_distance, con_highest) = canditates_off_bottom[0]
                    blackbox = cv2.minAreaRect(contours_blk[con_highest])
                else:
                    (y_highest, con_highest, x_min, y_min) = canditates[contours_blk_len - 1]
                    blackbox = cv2.minAreaRect(contours_blk[con_highest])
            (x_min, y_min), (w_min, h_min), ang = blackbox
            x_last = x_min
            y_last = y_min
            if ang < -45:
                ang = 90 + ang
            if w_min < h_min and ang > 0:
                ang = (90 - ang) * -1
            if w_min > h_min and ang < 0:
                ang = 90 + ang

            setpoint = 72
            error = int(x_min - setpoint)
            ang = int(ang)

            steer = int(((error*kp) + (ang*ap) + maxSteer)/(2*maxSteer) * 128)
            ser.write(str.encode(chr(127-steer)))


            print(steer)
            box = cv2.boxPoints(blackbox)
            box = np.int0(box)

            cv2.drawContours(image, [box], 0, (0, 0, 255), 3)
            cv2.putText(image, str(ang), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(image, str(error), (10, 72), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.line(image, (int(x_min), 72), (int(x_min), 82), (255, 0, 0), 3)

        else :
            ser.write(str.encode(chr(128)))

    cv2.imshow("orginal with line", image)
    TotalTime = time.time() - seconds
    a = a + 1
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
ser.write(str.encode(chr(0)))
seconds = TotalTime
print("Frames: " + str(a))
print("Seconds: " + str(seconds))
fps = a / seconds
print("fps: " + str(fps))

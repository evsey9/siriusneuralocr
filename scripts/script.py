import cv2
import os
import numpy as np
from skimage import io
cascpath = "data/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascpath)
def main(url = "http://www.highdefpeople.com/wp-content/uploads/2015/08/HERO-HD-People.jpg"):
    msg = ""
    imgarray = []
    image = io.imread(url)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1,minNeighbors=5,minSize=(30,30))
    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w, y+h), (255,255,255))
        cv2.imwrite('tempimg.png', image[y:y + h, x:x + w])
        imgarray.append(open('tempimg.png'))
    #cv2.imshow("Faces found", cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if (faces>0):
        msg = "Лицы найдены:"

    return(msg, imgarray)
    #cv2.waitKey(0)
    #return("Script run successful.")
#main()
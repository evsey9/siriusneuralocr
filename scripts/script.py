import cv2
import os
import numpy as np
from skimage import io
cascpath = "data/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascpath)
def main(url = "", *kwargs):
    if (url==""):
        return ["Пожалуйста введите URL изображения."]
    i = 0
    msg = ""
    imgarray = []
    try:
        image = io.imread(url)
    except:
        msg = "Введите правильный URL."
        return(msg)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1,minNeighbors=5,minSize=(30,30))
    for (x,y,w,h) in faces:
        #cv2.rectangle(image,(x,y),(x+w, y+h), (255,255,255))
        cv2.imwrite('tempimg'+str(i)+'.png', image[y:y + h, x:x + w])
        #imgfile = open('tempimg'+i+'.png')
        imgarray.append('tempimg'+str(i)+'.png')
        i += 1
        #imgfile.close
        #os.remove('tempimg.png')
    #cv2.imshow("Faces found", cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if (faces.size > 0):
        msg = "Лица найдены, подождите:"
    else:
        msg = "Лица не найдены."
    return[msg, *imgarray]
    #cv2.waitKey(0)
    #return("Script run successful.")
#main()
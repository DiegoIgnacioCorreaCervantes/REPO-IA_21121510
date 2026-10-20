import numpy as np
import cv2 as cv

rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')
cap = cv.VideoCapture('Videos/video4.mp4')
x=y=w=h= 0 
img = 0
count = 0
while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, 1.3, 5)
    for(x, y, w, h) in rostros:
        #m= int(h/2)
        img =  frame[y:y+h,x:x+w]

        img = cv.resize(img, (100, 100), interpolation=cv.INTER_CUBIC)

        count = count + 1 
        name = 'Dataset/Lucia/lucia_'+str(count)+'.jpg'
        cv.imwrite(name, img)
        frame = cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
        #frame = cv.rectangle(frame, (x,y+m), (x+w, y+h), (255, 0 ,0), 2 )
        cv.imshow('cara', img)
    
    cv.imshow('rostros', frame)
    
    
    k = cv.waitKey(1)
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()
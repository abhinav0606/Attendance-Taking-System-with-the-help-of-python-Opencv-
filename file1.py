import cv2
import os
Name=input("Enter the name of the Student")
id=input("Enter the id of the student")
folder=Name.lower()+id.lower()
try:
    os.mkdir("/home/abhinav/PycharmProjects/Attendance System with the help of opencv]/"+folder)
except:
    print("Folder Already exist")
    exit()
faces=cv2.CascadeClassifier("frontal_face.xml")
Capture=cv2.VideoCapture(0)
count=0
while True:
    ret,frame=Capture.read()
    frame=cv2.flip(frame,1)
    grey_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    face=faces.detectMultiScale(grey_frame,1.3,5)
    for (x,y,w,h) in face:
        cv2.imshow("Cropped",frame[y:y+h,x:x+w])
        cv2.imwrite("/home/abhinav/PycharmProjects/Attendance System with the help of opencv]/"+folder+"/"+str(count)+".JPG",cv2.cvtColor(frame[y:y+h,x:x+w],cv2.COLOR_BGR2GRAY))
        count=count+1
    if cv2.waitKey(1)==13 or count==100:
        break
Capture.release()
cv2.destroyAllWindows()
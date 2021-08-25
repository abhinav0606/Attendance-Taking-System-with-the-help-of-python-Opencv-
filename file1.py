import cv2
import os
id=input("Enter the id of the student")
folder=id.lower()
try:
    os.mkdir(r"C:\Users\\abhin\Desktop\Projects\Attendance-Taking-System-with-the-help-of-python-Opencv-\\"+folder)
except:
    print("Folder Already exist")
    exit()
faces=cv2.CascadeClassifier("frontal_face.xml")
Capture=cv2.VideoCapture(0,cv2.CAP_DSHOW)
count=1
while True:
    ret,frame=Capture.read()
    frame=cv2.flip(frame,1)
    grey_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    face=faces.detectMultiScale(grey_frame,1.3,5)
    for (x,y,w,h) in face:
        frame=cv2.putText(frame,str(count),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),thickness=2)
        frame=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),thickness=3)
        cv2.imshow("Frame",frame)
        cv2.imwrite(r"C:\Users\\abhin\Desktop\Projects\Attendance-Taking-System-with-the-help-of-python-Opencv-\\"+folder+"\\"+str(count)+".JPG",cv2.cvtColor(frame[y:y+h,x:x+w],cv2.COLOR_BGR2GRAY))
        count=count+1
    if cv2.waitKey(1)==13 or count==400:
        break
Capture.release()
cv2.destroyAllWindows()
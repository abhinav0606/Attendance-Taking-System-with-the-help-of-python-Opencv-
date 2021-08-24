import os
import cv2
import numpy as np
import datetime
import xlsxwriter
import pandas as pd
listing=str(datetime.datetime.now())
date=listing.split(" ")[0]
print(date)
Name=input("Enter the name of the Student")
Id=input("Enter the id of the student")
folder=Name.lower()+Id.lower()
list_files=os.listdir("C:\Users\\abhin\Desktop\Projects\Attendance-Taking-System-with-the-help-of-python-Opencv-\\"+folder)
list_files.sort()
print(list_files)
l=[]
t=[]
for i in range(len(list_files)):
    image_path="C:\Users\\abhin\Desktop\Projects\Attendance-Taking-System-with-the-help-of-python-Opencv-\\"+folder+"\\"+list_files[i]
    print(image_path)
    image=cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
    t.append(np.asarray(image,dtype=np.uint8))
    l.append(i)
l=np.asarray(l,dtype=np.int32)
model=cv2.face.LBPHFaceRecognizer_create()
model.train(np.asarray(t),np.asarray(l))
faces=cv2.CascadeClassifier("frontal_face.xml")
capture=cv2.VideoCapture(0)
result=0
attendence=[]
while True:
    try:
        ret,frame=capture.read()
        grey_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        face=faces.detectMultiScale(grey_frame,1.3,5)
        for (x,y,w,h) in face:
            cv2.imshow("Croppped",frame[y:y+h,x:x+w])
            result=model.predict(cv2.cvtColor(frame[y:y+h,x:x+w],cv2.COLOR_BGR2GRAY))
        confidence=0
        if result[1]<500:
            confidence = int(100 * ((1 - result[1] / 300)))
        if confidence>75:
            cv2.putText(frame, "unlocked "+str(confidence), (400, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
            # cv2.putText(frame, (100, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            attendence.append("Present")
        else:
            cv2.putText(frame, "locked "+str(confidence), (400, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
            attendence.append("Absent")
        cv2.imshow("Frame", frame)
    except:
        pass

    if cv2.waitKey(1)==13 or len(attendence)==120:
        break
print(attendence)
if attendence.count("Present")>77:
    listy=str(datetime.datetime.now())
    date=listy.split(" ")[0]
    excel_data=pd.read_excel("a.xlsx")
    columns_excell=list(excel_data.columns)
    print(columns_excell)
    workbook=xlsxwriter.Workbook("a.xlsx")
    worksheet=workbook.add_worksheet()
    worksheet.set_column(0,40,25)
    bold = workbook.add_format({'bold': True})
    for i in range(len(columns_excell)):
        print(columns_excell[i])
        worksheet.write(0,i,columns_excell[i],bold)
        for j in range(len(excel_data[columns_excell[i]])):
            worksheet.write(j+1,i,excel_data[columns_excell[i]][j])
    if date in columns_excell:
        index = columns_excell.index(date)
        worksheet.write(len(excel_data[date])+1, index, Id)
    else:
        if columns_excell == []:
            worksheet.write(0, len(columns_excell), date, bold)
            worksheet.write(1, len(columns_excell), Id)
        else:
            worksheet.write(0, len(columns_excell), date, bold)
            worksheet.write(1, len(columns_excell), Id)
    workbook.close()
capture.release()
cv2.destroyAllWindows()

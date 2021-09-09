from flask import Flask
from flask import render_template
from flask import Response
from flask import request
import cv2
import os
import datetime
import xlsxwriter
import numpy as np
import warnings
app=Flask(__name__)
faces=cv2.CascadeClassifier("frontal_face.xml")
def gen_dataset(folder):
    capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    count=1
    while True:
            success, frame = capture.read()
            frame=cv2.flip(frame,1)
            grey_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            face=faces.detectMultiScale(grey_frame,1.3,5)
            for (x,y,w,h) in face:
                frame = cv2.putText(frame, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), thickness=2)
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), thickness=3)
                cv2.imwrite(r"C:\Users\\abhin\Desktop\Projects\Attendance-Taking-System-with-the-help-of-python-Opencv-\\" + folder + "\\" + str(count) + ".JPG", cv2.cvtColor(frame[y:y + h, x:x + w], cv2.COLOR_BGR2GRAY))
                count = count + 1
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                if count==400:
                    break
                else:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            if count==400:
                break
    capture.release()
    cv2.destroyAllWindows()
    return "Done!"
def take_attendace(folder):
    capture=cv2.VideoCapture(0,cv2.CAP_DSHOW)
    list_files=os.listdir(r"C:\Users\\abhin\Desktop\Projects\Attendance-Taking-System-with-the-help-of-python-Opencv-\\"+folder)
    list_files.sort()
    l=[]
    t=[]
    for i in range(len(list_files)):
        image_path = r"C:\Users\\abhin\Desktop\Projects\Attendance-Taking-System-with-the-help-of-python-Opencv-\\" + folder + "\\" +list_files[i]
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        t.append(np.asarray(image, dtype=np.uint8))
        l.append(i)
    l=np.asarray(l,dtype=np.int32)
    warnings.filterwarnings("ignore",category=np.VisibleDeprecationWarning)
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(np.asarray(t), np.asarray(l))
    capture=cv2.VideoCapture(0,cv2.CAP_DSHOW)
    result=0
    attendance=[]
    while True:
        ret,frame=capture.read()
        frame=cv2.flip(frame,0)
        grey_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        face=faces.detectMultiScale(grey_frame,1.3,5)
        for (x,y,w,h) in face:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), thickness=3)
            result=model.predict(cv2.cvtColor(frame[y:y+h,x:x+w],cv2.COLOR_BGR2GRAY))
            confidence=0
            if result[1] < 500:
                confidence = int(100 * ((1 - result[1] / 300)))
            if confidence > 75:
                cv2.putText(frame, "unlocked " + str(confidence), (400, 450), cv2.FONT_HERSHEY_COMPLEX, 1,(255, 0, 255), 2)
                attendance.append("Present")
            else:
                cv2.putText(frame, "locked " + str(confidence), (400, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255),2)
                attendance.append("Absent")
            if len(attendance)==100:
                break
            else:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        if len(attendance)==100:
            break
    print(attendance)
    capture.release()
    cv2.destroyAllWindows()
    return "Done!!!"

@app.route('/')
def index():
    return render_template('index.html')
@app.route("/",methods=["POST"])
def index_post():
    global login_folder
    login_id=request.form.get("login_id")
    login_folder=login_id.lower()
    try:
        os.mkdir(r"C:\Users\\abhin\Desktop\Projects\Attendance-Taking-System-with-the-help-of-python-Opencv-\\" +login_folder)
    except:
        return login_folder
    return "Folder Already Exists!!!!"

@app.route('/video_feed')
def video_feed():
    # return name
    return Response(gen_dataset(folder), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/register")
def register():
    return render_template("register.html")
@app.route("/register",methods=["POST"])
def register_post():
    global folder
    college_id=request.form.get("ids")
    folder=college_id.lower()
    try:
        os.mkdir(r"C:\Users\\abhin\Desktop\Projects\Attendance-Taking-System-with-the-help-of-python-Opencv-\\" + folder)
    except:
        return "Folder Already Exist!"
    return render_template("register_view.html",folder=folder)
app.run(debug=True)
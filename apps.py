from flask import Flask
from flask import render_template
from flask import Response
from flask import request
import cv2
import os
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
    return "Folder Already Exists"

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
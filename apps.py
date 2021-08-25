from flask import Flask,render_template,Response
import cv2
app=Flask(__name__)
faces=cv2.CascadeClassifier("frontal_face.xml")
def gen_dataset():
    capture = cv2.VideoCapture(0)
    while True:
        success, frame = capture.read()
        frame=cv2.flip(frame,1)
        grey_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        face=faces.detectMultiScale(grey_frame,1.3,5)
        if not success:
            break
        else:
            for (x,y,w,h) in face:
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), thickness=3)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video_feed')
def video_feed():
    return Response(gen_dataset(), mimetype='multipart/x-mixed-replace; boundary=frame')
app.run(debug=True)
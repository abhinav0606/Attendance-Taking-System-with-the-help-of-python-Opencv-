# Attendance-Taking-System-with-the-help-of-python-Opencv-


Modules Used:

Opencv
os
numpy
xlsxwriter
pandas


#file1
In this file with the help of opencv we will create 100 samples of images of our face and will store(write) them in a specific folder((id+name).lower())
#file2
In this file we will take the id and name of the student and we will search for the folder that we have created in #file1
after this we will create a asarray of images and will create a model of the images(The images should be in grayscale) and afterthat with the help of opencv(Videocapture(0))
we will detect our face and crop it and with the help of model we will predict the face if it matches or not then we will calculate the result that if result is greater than 75
then the face matched otherwise not.
And after that we will update all the things in the excell file(xlsxwriter and pandas) the excell file is updated automatically.

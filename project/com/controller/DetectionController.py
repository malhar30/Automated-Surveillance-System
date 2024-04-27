import os
from datetime import datetime
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from flask import render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import random
from pathlib import Path
import cv2
import face_recognition
import numpy as np
from project import app
import requests
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.DetectionDAO import DetectionDAO
from project.com.vo.DetectionVO import DetectionVO
from project.com.dao.FaceDAO import FaceDAO
from project.com.vo.FaceVO import FaceVO


@app.route('/admin/viewDetection')
def adminViewDetection():
    try:
        if adminLoginSession() == "admin":
            detectionDAO = DetectionDAO()
            detectionVOList = detectionDAO.viewDetection()
            return render_template('admin/viewDetection.html',detectionVOList=detectionVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/user/viewDetection')
def userViewDetection():
    try:
        if adminLoginSession() == "user":
            detectionDAO = DetectionDAO()
            detectionVOList = detectionDAO.viewDetection()
            detectionVOList.reverse()
            return render_template('user/viewDetection.html',detectionVOList=detectionVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/user/trainDataset')
def get_encoded_faces():
    try:


        encoded = {}

        for dirpath, dnames, fnames in os.walk("project/static/dataset"):
            for f in fnames:
                if f.endswith(".jpg") or f.endswith(".png"):
                    face = face_recognition.load_image_file("project/static/dataset/"+f)
                    encoding = face_recognition.face_encodings(face)[0]
                    encoded[f.split(".")[0]] = encoding


        return encoded


    except Exception as ex:
        print(ex)

@app.route('/user/loadLive')
def userLive():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/userLive.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/live')
def userLoadLive():
    try:
        if adminLoginSession() == 'user':
            person_name={0}
            video_capture = cv2.VideoCapture(0)
            video_capture.set(3, 1920)
            video_capture.set(4, 1080)
            # 'http://192.168.43.1:8080/video'
            # fps=int(video_capture.get(5))
            fourcc = cv2.VideoWriter_fourcc(*'vp80')
            filepath = "project/static/adminResource/detection/"
            filename = ''.join((random.choice(string.digits)) for x in range(8))

            out = cv2.VideoWriter(filepath+filename+".webm", fourcc, 8, (640, 480))

            faces = get_encoded_faces()
            faces_encoded = list(faces.values())
            known_face_names = list(faces.keys())

            face_locations = []
            face_encodings = []
            face_names = []
            process_this_frame = True

            while True:

                ret, frame = video_capture.read()
                # frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.28)
                # small_frame = frame.copy()
                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]
                # rgb_small_frame = frame.copy()
                # Only process every other frame of video to save time
                if process_this_frame:
                    # Find all the faces and face encodings in the current frame of video
                    face_locations = face_recognition.face_locations(rgb_small_frame)
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                    face_names = []
                    for face_encoding in face_encodings:
                        # See if the face is a match for the known face(s)
                        matches = face_recognition.compare_faces(faces_encoded, face_encoding, tolerance=0.49)
                        name = "Unknown"

                        # Or instead, use the known face with the smallest distance to the new face
                        face_distances = face_recognition.face_distance(faces_encoded, face_encoding)

                        best_match_index = np.argmin(face_distances)

                        if matches[best_match_index]:
                            name = known_face_names[best_match_index]
                        # if name == 'Unknown':
                        #     playsound('project/static/adminResource/beep-01a.mp3')


                        face_names.append(name)
                        person_name.add(name)

                process_this_frame = not process_this_frame

                # Display the results
                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                    # Draw a box around the face
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                    # Draw a label with a name below the face
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                    out.write(frame)
                    cv2.imwrite("project/static/adminResource/face/" + name + ".jpg", frame)

                # Display the resulting image
                cv2.imshow("",frame)

                # Hit 'q' on the keyboard to quit!
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # Release handle to the webcam
            video_capture.release()
            cv2.destroyAllWindows()

            detectionDAO=DetectionDAO()
            detectionVO=DetectionVO()

            uploadDate = datetime.today().strftime("%d/%m/%Y")

            uploadTime = datetime.now().strftime("%H:%M:%S")

            detectionVO.detectionFileName = filename+".webm"
            detectionVO.detectionFilePath = filepath.replace('project','..')
            detectionVO.detectionUploadDate = uploadDate
            detectionVO.detectionUploadTime = uploadTime
            detectionVO.detection_LoginId = session['session_loginId']

            detectionDAO.insertDetection(detectionVO)
            userUsernameVOList=detectionDAO.viewLoginUser()
            userContactVOList=detectionDAO.viewRegisterUser()

            person_name_list=list(person_name)

            

            for face_name in person_name_list:
                if face_name != 0:
                    faceDAO = FaceDAO()
                    faceVO = FaceVO()
                    UPLOAD_FOLDER_USER = "project/static/adminResource/face/"
                    app.config['UPLOAD_FOLDER_USER'] = UPLOAD_FOLDER_USER
                    faceName=face_name
                    faceFileName=str(face_name)+".jpg"
                    faceFilePath = os.path.join(app.config['UPLOAD_FOLDER_USER'])
                    faceUploadDate = datetime.today().strftime("%d/%m/%Y")
                    faceUploadTime = datetime.now().strftime("%H:%M:%S")

                    faceVO.faceName=faceName
                    faceVO.faceFileName=faceFileName
                    faceVO.faceFilePath=faceFilePath.replace("project","..")
                    faceVO.faceUploadDate=faceUploadDate
                    faceVO.faceUploadTime=faceUploadTime

                    faceDAO.insertFace(faceVO)

            for i in person_name_list:
                if i == "Unknown":
                    for j in userUsernameVOList:
                        sender = "automatesurveillancesystem@gmail.com"

                        receiver =j.loginUsername

                        msg = MIMEMultipart()

                        msg['From'] = sender

                        msg['To'] = receiver

                        msg['Subject'] = "Alert"

                        msg.attach(MIMEText("Unknown person was detcted.", 'plain'))

                        # filename = filename+".webm"
                        # attachment = open("project/static/adminResource/detection/"+filename, "rb")
                        #
                        # # instance of MIMEBase and named as p
                        # p = MIMEBase('application', 'octet-stream')
                        #
                        # # To change the payload into encoded form
                        # p.set_payload((attachment).read())
                        #
                        # # encode into base64
                        # encoders.encode_base64(p)
                        #
                        # p.add_header('Content-Disposition', "attachment", filename=filename)
                        #
                        # # attach the instance 'p' to instance 'msg'
                        # msg.attach(p)

                        server = smtplib.SMTP('smtp.gmail.com', 587)

                        server.starttls()

                        server.login(sender, "m@lh@r3003")

                        text = msg.as_string()

                        server.sendmail(sender, receiver, text)

                        server.quit()

                    for number in userContactVOList:


                        url = "https://www.fast2sms.com/dev/bulk"

                        payload = "sender_id=FSTSMS&message=Alert!%20Unkown%20person%20was%20detected%20!%20&language=english&route=p&numbers={}".format(number.registerContactNumber)


                        headers = {
                            'authorization': "R9684WMwIZfsxX2vPr5FTQmuNg1l7VOEizC3eaqBHUdKStybnG6IUo9VXLNdhp1FKHD34Av8kuegZ2CM",
                            'Content-Type': "application/x-www-form-urlencoded",
                            'Cache-Control': "no-cache",
                        }

                        response = requests.request("POST", url, data=payload, headers=headers)

            return redirect(url_for('userLive'))


        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)

@app.route('/admin/deleteDetection',methods=['get'])
def adminDeleteDetection():
    try:
        if adminLoginSession() == 'admin':
            detectionDAO=DetectionDAO()
            detectionVO=DetectionVO()
            detectionId = request.args.get('detectionId')
            detectionVO.detectionId=detectionId
            detectionVOList = detectionDAO.deleteDetection(detectionVO)

            detectionFileName=detectionVOList.detectionFileName
            detectionFilePath=detectionVOList.detectionFilePath
            fullpath = detectionFilePath.replace('..','project') + detectionFileName
            os.remove(fullpath)
            return redirect(url_for('adminViewDetection'))

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

# @app.route('/user/insertVideo', methods=['POST'])
# def userInsertVideo():
#     try:
#         if adminLoginSession() == 'user':
#
#             UPLOAD_FOLDER = "project/static/adminResource/video/"
#             app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
#             file = request.files['file']
#
#             videoFileName = secure_filename(file.filename)
#
#             videoFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
#
#             file.save(os.path.join(videoFilePath, videoFileName))
#
#             videoUploadDate = datetime.today().strftime("%d/%m/%Y")
#
#             videoUploadTime = datetime.now().strftime("%H:%M:%S")
#             video_LoginId = session['session_loginId']
#
#             videoDAO = VideoDAO()
#             videoVO = VideoVO()
#
#             videoVO.videoFileName = videoFileName
#             videoVO.videoFilePath = videoFilePath.replace('project', "..")
#             videoVO.videoUploadDate = videoUploadDate
#             videoVO.videoUploadTime = videoUploadTime
#             videoVO.video_LoginId = video_LoginId
#
#             videoDAO.userInsertVideo(videoVO)
#
#             video_capture = cv2.VideoCapture(os.path.join(videoFilePath, videoFileName))
#             fps = int(video_capture.get(5))
#             width = int(video_capture.get(4))
#             height = int(video_capture.get(3))
#
#             fourcc = cv2.VideoWriter_fourcc(*'vp80')
#             out = cv2.VideoWriter("project/static/adminResource/detection/" + videoFileName + ".webm", fourcc, fps, (height, width))
#
#             faces = get_encoded_faces()
#             faces_encoded = list(faces.values())
#             known_face_names = list(faces.keys())
#
#             face_locations = []
#             face_encodings = []
#             face_names = []
#             process_this_frame = True
#
#             while True:
#                 ret, frame = video_capture.read()
#
#                 # Resize frame of video to 1/4 size for faster face recognition processing
#                 small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.28)
#                 # scale=60
#                 # width=int(frame.shape[1]*scale/100)
#                 # height=int(frame.shape[0]*scale/100)
#                 # dim=(width,height)
#                 #
#                 # small_frame=cv2.resize(frame,dim,interpolation=cv2.INTER_AREA)
#
#                 # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
#                 rgb_small_frame = small_frame[:, :, ::-1]
#                 # rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#                 # Only process every other frame of video to save time
#                 if process_this_frame:
#                     # Find all the faces and face encodings in the current frame of video
#                     face_locations = face_recognition.face_locations(rgb_small_frame)
#                     face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
#
#                     face_names = []
#                     for face_encoding in face_encodings:
#                         # See if the face is a match for the known face(s)
#                         matches = face_recognition.compare_faces(faces_encoded, face_encoding, tolerance=0.6)
#                         name = "Unknown"
#                         # Or instead, use the known face with the smallest distance to the new face
#                         face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
#                         best_match_index = np.argmin(face_distances)
#                         if matches[best_match_index]:
#                             name = known_face_names[best_match_index]
#                         print(name)
#                         face_names.append(name)
#
#                 process_this_frame = not process_this_frame
#
#                 # Display the results
#                 for (top, right, bottom, left), name in zip(face_locations, face_names):
#                     # Scale back up face locations since the frame we detected in was scaled to 1/4 size
#                     top *= 4
#                     right *= 4
#                     bottom *= 4
#                     left *= 4
#
#                     # Draw a box around the face
#                     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
#
#                     # Draw a label with a name below the face
#                     cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
#                     font = cv2.FONT_HERSHEY_DUPLEX
#                     cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
#                     out.write(frame)
#
#                 # Display the resulting image
#                 cv2.imshow('Video', frame)
#
#                 # Hit 'q' on the keyboard to quit!
#                 if cv2.waitKey(1) & 0xFF == ord('q'):
#                     break
#
#             # Release handle to the webcam
#             video_capture.release()
#             cv2.destroyAllWindows()
#
#             return redirect(url_for('userViewVideo'))
#
#
#         else:
#             return adminLogoutSession()
#     except Exception as ex:
#         print(ex)



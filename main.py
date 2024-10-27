#In future turn it into a web application using opencv.js
#dlib library is used to use GPU in the model cuda is used
#https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78

import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime



cred = credentials.Certificate("serviceaccountkey.json")
firebase_admin.initialize_app(cred,{
     #remove gs://
})#this is json format


bucket = storage.bucket()


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)


imgBackground = cv2.imread('Resources/background.png')


# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))


# Load the encoding file
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
# print(studentIds)
print("Encode File Loaded")

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:#this is the main loop which will continue every thing
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("matches", matches)
            # print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)#this will give minimum face distance the minimum = true = facerecognized
            # print("Match Index", matchIndex)

            if matches[matchIndex]:#The if loop for aftermath of face mathed
                # print("Known Face Detected")
                # print(studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:

            if counter == 1:
                # Get the Data
                studentInfo = db.reference(f'Students/{id}').get()#to get the student data from firebase database and the bucket
                print(studentInfo)
                # Get the Image from the storage
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                # Update data of attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                   "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()#it will be in seconts may be there is function to convert it in hour
                print(secondsElapsed)
                if secondsElapsed > 30:#time shold be in seconds
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 3:

                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                #This is the loop which will put the values on the right side background images
                if counter <= 10:
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

                    cv2.putText(imgBackground, str(studentInfo['Department']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                    cv2.putText(imgBackground, str(studentInfo['PRN']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    imgBackground[175:175 + 216, 909:909 + 216] = imgStudent
                    #print(studentInfo['name',])
                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0
    #cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)

    import pandas as pd
    from datetime import datetime


    # Initialize an empty DataFrame or load an existing Excel file
    def initialize_attendance_file(file_name):
        try:
            # Try to load an existing Excel file
            attendance_df = pd.read_excel("images/Book1.xlsx")
            print("Attendance file loaded successfully.")
        except FileNotFoundError:
            # If file doesn't exist, create a new DataFrame with relevant columns
            attendance_df = pd.DataFrame(columns=["Student ID", "Name", "Attendance Time", "Total Attendance"])
            print("New attendance file created.")

        return attendance_df


    # Function to record attendance in real-time
    def record_attendance(student_id, name, total_attendance, attendance_file):
        attendance_file = 'images/Book1.xlsx'
        # Load or initialize the attendance DataFrame
        attendance_df = initialize_attendance_file(attendance_file)

        # Get the current time
        attendance_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create a new record for the student
        new_record = {"Student ID": student_id, "Name": name, "Attendance Time": attendance_time,
                      "Total Attendance": total_attendance}

        # Append the new record to the DataFrame
        attendance_df = attendance_df.append(new_record, ignore_index=True)

        # Save the DataFrame back to the Excel file
        attendance_df.to_excel(attendance_file, index=False, engine='openpyxl')  # You missed passing the filename
        print(f"Attendance recorded for {name} at {attendance_time}")
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    # Example usage











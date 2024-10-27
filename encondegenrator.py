
import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from more_itertools.more import bucket
from numpy.core.multiarray import busday_offset


cred = credentials.Certificate("")
firebase_admin.initialize_app(cred,{
     #remove gs://
})#this is json format

# Importing student images
folderPath = 'Images'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []

for path in pathList:
    img = cv2.imread(os.path.join(folderPath, path))

    if img is None:
        print(f"Image at path {path} could not be loaded. Skipping.")
        continue  # Skip this iteration if the image could not be loaded

    imgList.append(img)
    studentIds.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print(studentIds)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)

        if len(encode) > 0:
            encodeList.append(encode[0])
        else:
            print(f"Face encoding failed for one of the images.")

    return encodeList


print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate()
firebase_admin.initialize_app(cred,{

})#this is json format

ref = db.reference('Students')

#This is json format here name is key and
data = {
    "1080":
        {
            "name": "Utkarsh",
            "Department": "AI and Data science",
            "starting_year": 2024,
            "total_attendance": 7,
             "PRN": "2124UDSM10 ",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1079":
        {
            "name": "Parth shinde",
            "Department": "AI and Data science",
            "starting_year": 2024,
            "total_attendance": 9,
             "PRN": "2124UDSM1079 ",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1073":
        {
            "name": "Harshad Pawar",
            "Department": "AI and Data science",
            "starting_year": 2024,
            "total_attendance": 10,
             "PRN": "2124UDSM1073 ",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1046":
        {
            "name": "Atharva Londhe",
            "Department": "AI and Data science",
            "starting_year": 2024,
            "total_attendance": 9,
             "PRN": "2124UDSM1046 ",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1001":
        {
            "name": "Abhiraj Patil",
            "Department": "AI and Data science",
            "starting_year": 2024,
            "total_attendance": 10,
             "PRN": "2124UDSM1001 ",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1142":
        {
            "name": "Rushikesh Kolhe",
            "Department": "AI and Data science",
            "starting_year": 2024,
            "total_attendance": 11,
             "PRN": "2124UDSM1142 ",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1028":
        {
            "name": "Saish Shinde",
            "Department": "AI and Data science",
            "starting_year": 2024,
            "total_attendance": 9,
             "PRN": "2124UDSM1028 ",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1096":
        {
            "name": "Sanskar Phadwal",
            "Department": "AI and Data science",
            "starting_year": 2024,
            "total_attendance": 9,
             "PRN": "2124UDSM1096 ",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1050":
        {
            "name": "Atharva Joshi",
            "Department": "AI and Data science",
            "starting_year": 2024,
            "total_attendance": 12,
             "PRN": "2124UDSM1050 ",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1013":
        {
            "name": "Pranit Sadhaphal",
            "Department": "AI and Data science",
            "starting_year": 2024,
            "total_attendance": 9,
             "PRN": "2124UDSM1013 ",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1068":
        {
            "name": "Tanishq Pahade",
            "Department": "AI and Data science",
            "starting_year": 2024,
            "total_attendance": 9,
             "PRN": "2124UDSM1068 ",
            "year": 7,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1101":
        {
            "name": "Pranav Sarode",
            "Department": "AI and Data science",
            "starting_year": 2024,
            "total_attendance": 9,
             "PRN": "2124UDSM1101 ",
            "year": 7,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1085":
        {
            "name": "Anuj Mandalik",
            "Department": "AI and Data science",
            "starting_year": 2024,
            "total_attendance": 9,
             "PRN": "2124UDSM1085 ",
            "year": 8,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1103":
        {
            "name": "Gajanan Jadhav",
            "Department": "AI and Data science",
            "starting_year": 2024,
            "total_attendance": 9,
             "PRN": "2124UDSM1103 ",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1143":
        {
            "name": "Ketan Khanapure",
            "Department": "AI and Data science",
            "starting_year": 2024,
            "total_attendance": 9,
             "PRN": "2124UDSM1143 ",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        }
}

for key, value in data.items():
    ref.child(key).set(value)


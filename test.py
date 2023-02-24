import json
from bs4 import BeautifulSoup

def getClasses(fileName):
    with open(fileName, "rb") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    initRan = False
    init = ""
    
    subjects = []
    days = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": []}
    campuses = {"Livingston": [], "Busch": [], "C/D": [], "College Avenue": [], "Online": []}
    
    for subject in soup.find_all(class_="subject"): # for each subject

        subject_name = subject.find(class_="courseTitle").text.strip()
        if subject_name == init:
            break
        if not initRan:
            init = subject_name
            initRan = True
        
        sectionData = []

        for section in subject.find_all(class_="sectionData"): # for each section
            section_index = section.find(class_="sectionIndexNumber").text.strip()

            classDetails = []
            divs = section.select('.sectionMeetingTimesDiv div')
            for div in divs: # for each class
                if div.find(class_="meetingTimeDay") is not None:
                    day = div.find(class_="meetingTimeDay").text.strip()
                    time = div.find(class_="meetingTimeHours").text.strip().replace(" ", "")
                    campus = div.find(class_="meetingTimeCampus").text.strip()
                    room_number = div.find(class_="meetingTimeBuildingAndRoom").text.strip()

                    classDetails.append({
                        "day": day,
                        "time": time,
                        "campus": campus,
                        "room_number": room_number
                    })
                    if not any(c["name"] == subject_name and c["index"] == section_index and c["time"] == time and c["room_number"] == room_number for c in days[day]):
                        days[day].append({
                            "name": subject_name,
                            "index": section_index,
                            "time": time,
                            "campus": campus,
                            "room_number": room_number
                        })
                    
                    # Add class to campus list if it does not already exist
                    if not any(c["name"] == subject_name and c["index"] == section_index and c["day"] == day for c in campuses[campus]):
                        campuses[campus].append({
                            "name": subject_name,
                            "index": section_index,
                            "day": day,
                            "time": time,
                            "room_number": room_number
                        })
                else:
                    note = "Hours by arrangement"
                    campus = "N/A"
                    if div.find(class_="sectionMeetingTimesDiv") is not None:
                        note = "Asynchronous content"
                        campus = "Online"                     
                    classDetails.append({
                        "campus": campus,
                        "note": note
                    })

            sectionData.append({
                "index": section_index,
                "classes": classDetails
            })
                    
        subjects.append({
            "name": subject_name,
            "sectionData": sectionData
        })

    # Print the data for this file
    # print("File:", fileName)
    # for subject in subjects:
    #     print(subject["name"])
    #     for section in subject["sectionData"]:
    #         print(" Index:", section["index"])
    #         for classDetails in section["classes"]:
    #             try:
    #                 class_time = classDetails["time"]
    #                 class_campus = classDetails["campus"]
    #                 print("  ", class_time, "-", class_campus)
    #             except:
    #                 print("  ", classDetails["note"])
    # print()
    # print("Classes on Wednesday:")
    # for class_info in days["Wednesday"]:
    #     print(class_info["name"], "-", class_info["time"], "-", class_info["campus"])
    # # print online classes
    # print()
    # print("Classes on C/D:")
    # for class_info in campuses["C/D"]:
    #     print(class_info["name"], "-", class_info["day"], "-", class_info["time"])
    # print()
    # print("Classes on College Ave:")
    # for class_info in campuses["College Avenue"]:
    #     print(class_info["name"], "-", class_info["day"], "-", class_info["time"])

    return(subjects, days, campuses)
# Call the function for each HTML file
#getClasses("14_332.html")
#getClasses("01_840.html")
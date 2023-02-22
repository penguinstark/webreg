import json
from bs4 import BeautifulSoup

def getClasses(fileName):
    with open(fileName, "rb") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    initRan = False
    init = ""
    subjects = []

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
    # Add the data to the JSON file
    with open('class_data.json', 'a') as outfile:
        data = {
            "school": fileName.split(".")[0],
            "subjects": subjects
        }
        json.dump(data, outfile, indent=2)

    # Print the data for this file
    print("File:", fileName)
    for subject in subjects:
        print(subject["name"])
        for section in subject["sectionData"]:
            print(" Index:", section["index"])
            for classDetails in section["classes"]:
                try:
                    class_time = classDetails["time"]
                    class_campus = classDetails["campus"]
                    print("  ", class_time, "-", class_campus)
                except:
                    print("  ", classDetails["note"])
    
    print("\n")

# Call the function for each HTML file
getClasses("14_332.html")
getClasses("01_840.html")
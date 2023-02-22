from bs4 import BeautifulSoup

def getClasses(fileName):
    with open(fileName, "rb") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    initRan = False
    init = ""
    
    Monday, Tuesday, Wednesday, Thursday, Friday = [], [], [], [], []
    cd, busch, livi, ca, online = [], [], [], [], []
    subjects = []

    for subject in soup.find_all(class_="subject"): # for each subject

        subject_name = subject.find(class_="courseTitle").text.strip()
        if subject_name == init:
            break
        if not initRan:
            init = subject_name
            initRan = True
        print(subject_name)
        
        # print the number of sections in the each subject
        # print(len(subject.find_all(class_="sectionData")))

        for section in subject.find_all(class_="sectionData"): # for each section
            section_index = section.find(class_="sectionIndexNumber").text.strip()
            print(" Section Index:", section_index)
            eachClass = []
            # if sections contains the class "meetingTimeDay" then print the details
            divs = section.select('.sectionMeetingTimesDiv div')
            for div in divs: # for each class
                lastIndex = 0
                section = [] # section is a list of dictionaries (classDetails)
                if div.find(class_="meetingTimeDay") is not None:
                    day = div.find(class_="meetingTimeDay").text.strip()
                    time = div.find(class_="meetingTimeHours").text.strip().replace(" ", "")
                    campus = div.find(class_="meetingTimeCampus").text.strip()
                    room_number = div.find(class_="meetingTimeBuildingAndRoom").text.strip()
                    # store these values in a list with the index as the name of the list
                    classDetails = {"index": section_index, "name": subject_name, "day": day, "time": time, "campus": campus, "room_number": room_number}
                    
                    if lastIndex != section_index:
                        lastIndex = section_index
                        if day == "Monday": Monday.append(classDetails)
                        elif day == "Tuesday": Tuesday.append(classDetails)
                        elif day == "Wednesday": Wednesday.append(classDetails)
                        elif day == "Thursday": Thursday.append(classDetails)
                        elif day == "Friday": Friday.append(classDetails)
                    
                    print("  ", day, time)
                    section.append(classDetails)
                    # print("  Day:", day, "Time:", time, "Campus:", campus, "Room Number:", room_number)
                else:
                    try:
                        campus = div.find(class_="meetingTimeCampus").text.strip()
                        note = "Asynchronous content"
                    except: 
                        campus = "N/A"
                        note = "Hours by arrangement"
                    classDetails = {"index": section_index, "name": subject_name, "campus": campus, "note": note}
                    section.append(classDetails)
                if campus == "Busch": busch.append(section)
                elif campus == "Livingston": livi.append(section)
                elif campus == "College Avenue": ca.append(section)
                elif campus == "Online": online.append(section)
                elif campus == "CD": cd.append(section)
            eachClass.append(section)
        subjects.append(eachClass)
        # print('\n')

        # break for testing (COMMENT WHEN DONE)
        # break
    days = [Monday, Tuesday, Wednesday, Thursday, Friday]
    campuses = [cd, busch, livi, ca, online]
    return (subjects, days, campuses)

eceSubjects, eceDays, eceCampuses = getClasses('14_332.html')
religionSubjects, religionDays, religionCampuses = getClasses('01_840.html')

# for i in range(len(religionSubjects)): # list of subjects
#     for j in range(len(religionSubjects[i])): # list of eachClass
#         print(religionSubjects[i][j][0]["name"])
#         for k in range(len(religionSubjects[i][j])): # list of sections
#             print(religionSubjects[i][j][k]["index"])
# for i in range(len(eceSubjects)): # list of subjects
#     for j in range(len(eceSubjects[i])): # list of eachClass
#         print(eceSubjects[i][j][0]["name"])
#         for k in range(len(eceSubjects[i][j])): # list of sections
#             print(eceSubjects[i][j][k]["index"])
# for i in range(len(religionDays)):
#     for j in range(len(religionDays[i])):
#         print(religionDays[i][j]["campus"])
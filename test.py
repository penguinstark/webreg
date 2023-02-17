from bs4 import BeautifulSoup

with open("sample.html", "rb") as f:
    content = f.read()

soup = BeautifulSoup(content, "html.parser")
initRan = False
init = ""

for subject in soup.find_all(class_="subject"): # for each subject
    # print the subject name
    subject_name = subject.find(class_="courseTitle").text.strip()
    if subject_name == init:
        break
    if not initRan:
        init = subject_name
        initRan = True
    print("\n", subject_name)
    
    # print the number of sections in the each subject
    # print(len(subject.find_all(class_="sectionData")))

    for section in subject.find_all(class_="sectionData"): # for each section
        section_index = section.find(class_="sectionIndexNumber").text.strip()
        print("Section Index:", section_index)

        # if sections contains the class "sectionMeetingTimesDiv" then print the details
        for classes in section.find_all(class_="sectionMeetingTimesDiv"): # for each class
            try: day = classes.find(class_="meetingTimeDay").text.strip()
            except:
                print("No class times available")
                continue
            time = classes.find(class_="meetingTimeHours").text.strip()
            campus = classes.find(class_="meetingTimeCampus").text.strip()
            room_number = classes.find(class_="meetingTimeBuildingAndRoom").text.strip()
            print("Day:", day, "Time:", time, "Campus:", campus, "Room Number:", room_number)
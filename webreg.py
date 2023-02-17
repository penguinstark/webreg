from bs4 import BeautifulSoup

with open("sample.html", "r") as f:
    content = f.read()

soup = BeautifulSoup(content, "html.parser")

day_indices = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": [], "Saturday": []}
campus_indices = {"ON": [], "NB": [], "MC": [], "CD": [], "CM": [], "PG": [], "PV": []}
for subject in soup.find_all(class_="subject"):
    subject_code = subject.find(class_="subjectDataCode").text.strip()
    subject_name = subject.find(class_="subjectDataName").text.strip()
    print("Subject Code:", subject_code)
    print("Subject Name:", subject_name)
    for section in soup.find_all(class_="sectionListings"):
        section_number = section.find(class_="sectionDataNumber").text.strip()
        section_index = section.find(class_="sectionIndexNumber").text.strip()

        classes = []
        for cls in section.find_all(class_="sectionMeeting"):
            day = cls.find(class_="meetingTimeDay").text.strip()
            time = cls.find(class_="meetingTimeHours").text.strip()
            campus = cls.find(class_="meetingTimeCampus").text.strip()
            room_number = cls.find(class_="meetingTimeBuildingAndRoom").text.strip()
            classes.append({"day": day, "time": time, "campus": campus, "room_number": room_number})
            day_indices[day].append((section_number, section_index))
            campus_indices[campus].append((section_number, section_index))

    print("Section Number:", section_number)
    print("Section Index:", section_index)
    print("Classes:", classes)
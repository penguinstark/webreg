from bs4 import BeautifulSoup

with open("sample.html", "rb") as f:
    content = f.read()

soup = BeautifulSoup(content, "html.parser")
initRan = False
init = ""

for subject in soup.find_all(class_="subject"):
    # print the subject name
    subject_name = subject.find(class_="courseTitle").text.strip()
    if subject_name == init:
        break
    if not initRan:
        init = subject_name
        initRan = True
    print(subject_name)
    # for each subject print the section number and section index
    # print the numeber of  divs in the sectionListings class
    print(len(subject.find_all(class_="sectionData")))
    
    for section in subject.find_all(class_="sectionData"):
        section_index = section.find(class_="sectionIndexNumber").text.strip()
        print("Section Index:", section_index)
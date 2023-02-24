from test import getClasses
import json, os
def dayCampus (d, c):
    chosenDay = d
    chosenCampus = c
    # Add the data to the JSON file
    with open('class_data.json', 'a') as outfile:
        for fileName in os.listdir("."):
            if fileName.endswith('.html'):
                subjects, days, campuses = getClasses(fileName)
                dep = fileName.split(".")[0]
                data = {
                    "school": dep,
                    "subjects": subjects,
                    "days": days,
                    "campuses": campuses
                }
                json.dump(data, outfile, indent=2)
                print("Classes on", chosenDay, "at", chosenCampus, "for", dep)
                dcItems = []
                for i in range(len(chosenDay)):
                    for class_info in days[chosenDay[i]]:
                        for j in range(len(chosenCampus)):
                            if class_info["campus"] == chosenCampus[j]:
                                dcItems.append(class_info)
                    sorted_dcItems = sorted(dcItems, key=lambda x: x["time"])
                    for class_info in sorted_dcItems:
                        print(class_info["name"], "-", class_info["time"], "-", class_info["campus"])
                # for class_info in days["Wednesday"]:
                #     if class_info["campus"] == "College Avenue":
                #         print(class_info["name"], "-", class_info["time"], "-", class_info["campus"])
d = ["Friday"]
c = ["Busch", "Livingston", "College Avenue"]
dayCampus(d,c)
# getClasses("14_332.html")
# getClasses("01_840.html")

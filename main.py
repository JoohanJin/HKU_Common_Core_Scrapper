from bs4 import BeautifulSoup as bs
from requests import get
import csv

'''
course code
course name
description
outcomes
period of study
study load - table
assessment - table
required reading
lecturer 
'''

subjects = []

with open('lists.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        subjects.extend(row)
    
    file.close()
subjects = set(subjects)
print(len(subjects))

# for course_code in range(subject):
#     URL = f"https://commoncore.hku.hk/{course_code}/"
RESULTS = []

def get_info(keyword):
    URL = f"https://commoncore.hku.hk/{keyword}/"
    print(f"working on {keyword}!\n")
    response = get(URL)

    if (response.status_code != 200):
        print(response)
        print(f"could not get an information from {URL}")
    else:
        soup = bs(response.text, "html.parser")
        tables = soup.find_all("table")
        paras = soup.find_all("p")


        description = ""
        for i in range(len(paras)):
            text = paras[i].get_text().replace("\n", "")
            if (text == "On completing the course, students will be able to:"):
                course_period = paras[i+1].get_text()
                break
            elif len(text) > 2:
                description = description + f"{text}"
        

        course_title = soup.find('h1', class_='page-title').string

        lecturer_rows = tables[-1].find_all("tr")[1:]
        lecturers = ""
        for i in range(len(lecturer_rows)):
            data = lecturer_rows[i].find_all("td")
            name = data[0].get_text().replace("\n", " ")
            contact = data[1].get_text().replace("\n", " ")
            if contact != "Contact":
                lecturers = lecturers + f"- {name}: {contact}\n"
            elif (i == len(lecturer_rows) -1):
                lecturers = lecturers + f"- {name}: {contact}"


        assessment_table = tables[-2].find_all("tr")[1:]
        assessments = ""
        total = 0
        for assessment in assessment_table:
            data = assessment.find_all("td")
            title = data[0].get_text()
            point = data[1].get_text()
            total = total + int(point)
            if total < 100:
                assessments = assessments + f"- {title}: {point}\n"
            else:
                assessments = assessments + f"- {title}: {point}"

        workload_table = tables[-3].find_all("tr")[1:]
        workloads = ""
        for workload in workload_table:
            data = workload.find_all("td")
            title = data[0].get_text()
            time = data[1].get_text()
            if title != "Total:":
                workloads = workloads + f"- {title}: {time}\n"
            else:
                workloads = workloads + f"- {title} {time}"

        RESULTS.append(
            {
                "course_title": course_title,
                "description":  description,
                "course_period": course_period,
                "lecturer": lecturers,
                "assessment": assessments,
                "workload": workloads,
            }
        )

for subject in subjects:
    get_info(subject)

file = open(f"result.csv", "w")
file.write("Course_Title, Course_Description, Offer_Period, Lecturers, Assessments, Workloads\n")
for RESULT in RESULTS:
    file.write(f"\"{RESULT['course_title']}\",\"{RESULT['description']}\",\"{RESULT['course_period']}\",\"{RESULT['lecturer']}\",\"{RESULT['assessment']}\",\"{RESULT['workload']}\"\n")
print(f"finished writing on result.csv file")
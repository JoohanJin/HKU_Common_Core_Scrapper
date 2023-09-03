from bs4 import BeautifulSoup as bs
from requests import get
import csv


class Course:
    def __init__(self, course_code):
        self.course_code = course_code
        self.course_name = ""
        self.description = ""
        self.period_offer = ""
        self.study_load = ""
        self.assessment = ""
        self.lecturer = ""
    
    def display_info(self):
        print(f"Course code: {self.course_code}")
        print(f"Course name: {self.course_name}")
        print(f"Description: {self.description}")
        print(f"")



class Scrapper:
    def __init__(self):
        pass
    
    def read_course_info(self, course_code):
        URL = f"https://commoncore.hku.hk/{course_code}/"
        print(f"working on {course_code}!")       
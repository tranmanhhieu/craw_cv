# from linkedin_search_posts_bot import *
# from cookie import *
from selenium import webdriver
from linkedin_scraper import Person, actions
from selenium.webdriver.chrome.options import Options
import re
import datetime
import pymongo
import random
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

lnks = []
# # driver = webdriver.Chrome()
opts = Options()
driver = webdriver.Chrome(options=opts, executable_path='chromedriver')
for x in range(0, 20, 10):
    driver.get(
        f'https://www.google.com/search?q=site:linkedin.com/in/+AND+%22data+scientist%22+AND+%22Vietnam%22&rlz=1C1PNBB_enVN960VN960&sxsrf=APwXEdc15zXVXvz9D87tAev17eChXF60rQ:1684379702683&ei=NphlZMyVKYe32roP556rwAU&start={x}&sa=N&ved=2ahUKEwjMiOGu8_3-AhWHm1YBHWfPClgQ8tMDegQIHxAE&biw=1920&bih=979&dpr=1')
    time.sleep(random.uniform(2.5, 4.9))
    linkedin_urls = driver.find_elements(By.XPATH, '//div[@class="yuRUbf"]/a')
    for link in linkedin_urls:
        lnks.append(link.get_attribute('href'))
# print(lnks)
time.sleep(5)
from selenium.webdriver.firefox.options import Options

email = "beomik0123@gmail.com"
password = "beomik123"
actions.login(driver, email, password)
time.sleep(5)
myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["craw_cv"]

for i in lnks:
    data = {}
    try:
        person = Person(i, driver=driver, close_on_complete=False)
        data['url'] = person.linkedin_url
        data['name'] = person.name
        data['about'] = person.about
        data['company'] = person.company
        data['job_title'] = person.job_title
        data['experiences'] = []
        data['educations'] = []
        data['location'] = person.location
        exp = {}
        id_exp = 0
        for i in person.experiences:
            experiences = {}
            experiences['position_title'] = i.position_title
            experiences['from_date'] = i.from_date
            experiences['to_date'] = i.to_date
            experiences['duration'] = i.duration
            experiences['location'] = i.location
            experiences['description'] = i.description
            experiences['institution_name'] = i.institution_name
            experiences['linkedin_url'] = i.linkedin_url
            id_exp += 1
            exp[str(id_exp)] = experiences
        data['experiences'] = exp

        edu = {}
        id_edu = 0
        for i in person.educations:
            education = {}
            education['from_date'] = i.from_date
            education['to_date'] = i.to_date
            education['description'] = i.description
            education['degree'] = i.degree
            education['institution_name'] = i.institution_name
            education['linkedin_url'] = i.linkedin_url
            id_edu += 1
            edu[str(id_edu)] = education
        data['educations'] = edu

        mydb['linkedin_profile'].insert_one(data)
    except:
        pass
    print(data)

    time.sleep(10)


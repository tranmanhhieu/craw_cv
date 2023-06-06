from linkedin_search_posts_bot import *
from cookie import *
from linkedin_post_scraper_with_python import *
import pymongo
import random
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from linkedin_scraper import Person, actions


lnks = []
# # driver = webdriver.Chrome()
opts = Options()
driver = webdriver.Chrome(options=opts, executable_path='chromedriver')
myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["craw_cv"]

for x in range(0, 20, 10):
    driver.get(
        f'https://www.google.com/search?q=site:linkedin.com/posts/+inurl:/in/+intitle:data+science&rlz=1C1PNBB_enVN960VN960&sxsrf=APwXEdcEHsKS8i_rxEk_shM9UPJHZ2bvxw:1684831565326&ei=TX1sZIq9E92j2roPg-qkwA8&start={x}&sa=N&ved=2ahUKEwjKl9TXhov_AhXdkVYBHQM1CfgQ8tMDegQIDBAE&biw=958&bih=955&dpr=1')
    time.sleep(random.uniform(2.5, 4.9))
    linkedin_urls = driver.find_elements(By.XPATH, '//div[@class="yuRUbf"]/a')
    for link in linkedin_urls:
        lnks.append(link.get_attribute('href'))
# print(lnks)
time.sleep(5)

linkedin.login(email="beomik0123@gmail.com",password="beomik123")
# linkedin.login_cookie(cookies=cookies)
for lin in lnks:
    response=linkedin.get_post(post_link=lin)
    data=response['body']
    print(data)
    mydb['linkedin_post'].insert_one(data)
# response=linkedin.get_post(post_link="https://www.linkedin.com/posts/mengyaowang11_data-datascience-dataanalysis-activity-7066249399256944640-0MqX?utm_source=share&utm_medium=member_desktop")
# data=response['body']
# print(data)


# linkedin.search_posts(keyword='data science')
# all_data = []
# for i in range(0, 5):
#     response = linkedin.posts_results()
#     data = response['body']
#     # data=[{"User Link": "https://www.linkedin.com/in/ACoAAA-o4hwBSDzBqrYMLlBP_Z6a32-3OXHT1JE?lipi=urn%3Ali%3Apage%3Ad_flagship3_search_srp_content%3BeEN9bbddQ0KdHDbJSiRlNw%3D%3D", "Post Text": "My team at Amazon is hiring multiple data scientis.."},..]
#     all_data.extend(data)
#     linkedin.click_next()  # clicks in next button
# print(all_data)

# from linkedin_search_results import *
# linkedin.login(email="beomik0123@gmail.com",password="beomik123")
# # linkedin.login_cookie(cookies=cookies)
#
# response =linkedin.search_results(keyword="data science")
#
# print(response['body'])
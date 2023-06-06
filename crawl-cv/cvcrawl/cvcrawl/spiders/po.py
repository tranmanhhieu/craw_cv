from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import re as re

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import random


# access Webriver
opts = Options()
browser = webdriver.Chrome(options=opts, executable_path='chromedriver')

# lnks = []
# # # driver = webdriver.Chrome()
#
# for x in range(0, 20, 10):
#     browser.get(
#         f'https://www.google.com/search?q=site:linkedin.com/posts/+inurl:/in/+intitle:data+science&rlz=1C1PNBB_enVN960VN960&sxsrf=APwXEdcEHsKS8i_rxEk_shM9UPJHZ2bvxw:1684831565326&ei=TX1sZIq9E92j2roPg-qkwA8&start={x}&sa=N&ved=2ahUKEwjKl9TXhov_AhXdkVYBHQM1CfgQ8tMDegQIDBAE&biw=958&bih=955&dpr=1')
#     time.sleep(random.uniform(2.5, 4.9))
#     linkedin_urls = browser.find_elements(By.XPATH, '//div[@class="yuRUbf"]/a')
#     for link in linkedin_urls:
#         lnks.append(link.get_attribute('href'))
# # print(lnks)
# time.sleep(5)
# # Open login page

browser.get('https://www.linkedin.com')

# Enter login info:
username = browser.find_element(By.ID,'session_key')
username.send_keys("beomik0123@gmail.com")
time.sleep(0.5)

password = browser.find_element(By.ID,'session_password')
password.send_keys('beomik123')
time.sleep(0.5)

sign_in = browser.find_element(By.XPATH,'//*[@type="submit"]')
sign_in.click()
time.sleep(9)
# Note: replace the keys "username" and "password" with your LinkedIn login info



# In[28]:


# #Go to webpage
browser.get("https://www.linkedin.com/posts/mengyaowang11_data-datascience-dataanalysis-activity-7066249399256944640-0MqX?utm_source=share&utm_medium=member_desktop")

company_page = browser.page_source

# In[35]:


linkedin_soup = bs(company_page.encode("utf-8"), "html",features="lxml")
linkedin_soup.prettify()

containers = linkedin_soup.findAll("div", {"class": "occludable-update ember-view"})
# container = containers[0].find("div","display-flex feed-shared-actor display-flex feed-shared-actor--with-control-menu ember-view")


# In[36]:


post_dates = []
post_texts = []
post_likes = []
post_comments = []
video_views = []
media_links = []
media_type = []

for container in containers:

    try:
        posted_date = container.find("span", {"class": "visually-hidden"})
        text_box = container.find("div", {"class": "feed-shared-update-v2__description-wrapper"})
        text = text_box.find("span", {"dir": "ltr"})
        new_likes = container.findAll("li", {
            "class": "social-details-social-counts__reactions social-details-social-counts__item"})
        new_comments = container.findAll("li", {
            "class": "social-details-social-counts__comments social-details-social-counts__item"})

        post_dates.append(posted_date.text.strip())
        post_texts.append(text.text.strip())

        try:
            video_box = container.findAll("div", {
                "class": "feed-shared-update-v2__content feed-shared-linkedin-video ember-view"})
            video_link = video_box[0].find("video", {"class": "vjs-tech"})
            media_links.append(video_link['src'])
            media_type.append("Video")
        except:
            try:
                image_box = container.findAll("div", {"class": "feed-shared-image__container"})
                image_link = image_box[0].find("img", {
                    "class": "ivm-view-attr__img--centered feed-shared-image__image feed-shared-image__image--constrained lazy-image ember-view"})
                media_links.append(image_link['src'])
                media_type.append("Image")
            except:
                try:
                    # mutiple shared images
                    image_box = container.findAll("div", {"class": "feed-shared-image__container"})
                    image_link = image_box[0].find("img", {
                        "class": "ivm-view-attr__img--centered feed-shared-image__image lazy-image ember-view"})
                    media_links.append(image_link['src'])
                    media_type.append("Multiple Images")
                except:
                    try:
                        article_box = container.findAll("div", {"class": "feed-shared-article__description-container"})
                        article_link = article_box[0].find('a', href=True)
                        media_links.append(article_link['href'])
                        media_type.append("Article")
                    except:
                        try:
                            video_box = container.findAll("div", {"class": "feed-shared-external-video__meta"})
                            video_link = video_box[0].find('a', href=True)
                            media_links.append(video_link['href'])
                            media_type.append("Youtube Video")
                        except:
                            try:
                                poll_box = container.findAll("div", {
                                    "class": "feed-shared-update-v2__content overflow-hidden feed-shared-poll ember-view"})
                                media_links.append("None")
                                media_type.append("Other: Poll, Shared Post, etc")
                            except:
                                media_links.append("None")
                                media_type.append("Unknown")

        # Getting Video Views. (The folling three lines prevents class name overlap)
        view_container2 = set(container.findAll("li", {'class': ["social-details-social-counts__item"]}))
        view_container1 = set(container.findAll("li", {'class': ["social-details-social-counts__reactions",
                                                                 "social-details-social-counts__comments social-details-social-counts__item"]}))
        result = view_container2 - view_container1

        view_container = []
        for i in result:
            view_container += i

        try:
            video_views.append(view_container[1].text.strip().replace(' Views', ''))

        except:
            video_views.append('N/A')

        try:
            post_likes.append(new_likes[0].text.strip())
        except:
            post_likes.append(0)
            pass

        try:
            post_comments.append(new_comments[0].text.strip())
        except:
            post_comments.append(0)
            pass

    except:
        pass

# In[42]:


# cleaned_dates = []
# for i in post_dates:
#     d = str(i[0:3]).replace('\n\n', '').replace('•','').replace(' ', '')
#     cleaned_dates += [d]

comment_count = []
for i in post_comments:
    s = str(i).replace('comment', '').replace('s', '').replace(' ', '')
    comment_count += [s]

# In[43]:


# pd.set_option('max_colwidth', 1000)

data = {
    "Date Posted": post_dates,
    "Media Type": media_type,
    "Post Text": post_texts,
    "Post Likes": post_likes,
    "Post Comments": comment_count,
    "Video Views": video_views,
    "Media Links": media_links
}

df = pd.DataFrame(data)
print(df)
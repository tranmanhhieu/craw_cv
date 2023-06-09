import pymongo
import random
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import requests
from linkedin_scraper import Person, actions
import undetected_chromedriver as uc

#lấy proxy mới

def init_driver():
    response = requests.get('https://proxy.sodalab.dev/random')
    proxy = response.text.strip()

    opts = {
        'proxy': {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}',
        }
    }
    driver = uc.Chrome(seleniumwire_options=opts, executable_path='chromedriver')
    return driver

def is_captcha_present(driver):
    return len(driver.find_elements(By.XPATH, "//div[contains(@class, 'rc-anchor-error-msg')]")) > 0

def get_list_link(keyword,num_page):

    list_url = []
    key_word = "+".join(keyword.split(" "))
    end_page = 50

    while num_page <= end_page:
        #tạo mới driver
        driver = init_driver()
        driver.get(
            f'https://www.google.com/search?q=site:linkedin.com/posts/+inurl:/in/+intitle:{key_word}&rlz=1C1PNBB_enVN960VN960&sxsrf=APwXEdcEHsKS8i_rxEk_shM9UPJHZ2bvxw:1684831565326&ei=TX1sZIq9E92j2roPg-qkwA8&start={num_page}&sa=N&ved=2ahUKEwjKl9TXhov_AhXdkVYBHQM1CfgQ8tMDegQIDBAE&biw=958&bih=955&dpr=1')
        if is_captcha_present(driver):
            driver.quit()
            init_driver()
            return get_list_link(keyword,num_page)

        time.sleep(random.uniform(2.5, 4.9))
        linkedin_urls = driver.find_elements(By.XPATH, '//div[@class="yuRUbf"]/a')
        for link in linkedin_urls:
            list_url.append(link.get_attribute('href'))
        time.sleep(2)
        num_page += 10
        driver.quit()


    return list_url

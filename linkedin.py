import seleniumwire.undetected_chromedriver.v2 as uc
import chromedriver_autoinstaller
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from utils.utils import get_proxy, scroll_down
import random
import time 
from datetime import datetime

class LinkedinBot:
    def __init__(self, proxy=True, headless=False):
        chromedriver_autoinstaller.install()
        self.chrome_version = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
        self.driver = self._init_driver(proxy, headless)

    def _init_driver(self, proxy, headless):
        """Mở chương trình chrome

        Args:
            proxy(bool): True nếu dùng proxy và ngược lại
            headless(bool): True chạy bằng mode headless, default False
        """
        options = uc.ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--disable-gpu")
        if proxy:
            self.proxy = get_proxy()
            proxies = {
                'proxy': {
                    'http': f'http://{self.proxy}',
                    'https': f'http://{self.proxy}',
                    'no_proxy': 'localhost,127.0.0.1'
                }
            }
        if headless:
            options.add_argument("--headless")
        driver = uc.Chrome(options=options, 
                           version_main=self.chrome_version, 
                           seleniumwire_options=proxies
                           )
        return driver

    def get_post(self, post):
        """Lấy nội dung bài post bao gồm người đăng (user), thời gian (time) và nội dung (content)
        
        Args:
            post: post element

        Returns:
            Dict: Nội dung bài post
        """
        try:
            item = {}
            try:
                btn_more = post.find_elements('xpath', './/button[contains(text(), "...more")]')
                if btn_more:
                    ActionChains(self.driver).click(btn_more[0]).perform()
            except Exception as ex:
                pass 
            all_text = post.text.split('\n')
            item['user'] = all_text[0]
            item['time'] = all_text[2]
            item['content'] = '\n'.join(all_text[3:])
            item['crawled'] = datetime.now()
            return item
        except Exception as ex:
            return None 
    
    def get_posts(self):
        """Lấy danh sách bài post trên trang web hiển thị

        Return:
            List[dict]: Danh sách các bài post
        """
        results = []
        section = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "serp-page__results-list")))
        posts = section.find_elements('xpath', './ul/li')
        for post in posts:
            post = self.get_post(post)
            time.sleep(1)
            if post:
                print(post.get('user'))
                results.append(post)
        return results
    
    def search(self, keyword):
        """Lấy bài post theo keyword

        Args:
            keyword: Từ khóa tìm kiếm

        Returns:
            List[dict]: Danh sách các bài post
        """
        keyword = '%20'.join(keyword.split())
        url = f'https://www.linkedin.com/search/results/content/?keywords={keyword}'
        self.driver.get(url)
        time.sleep(random.randint(3,4))
        return self.get_posts()

if __name__ == '__main__':
    bot = LinkedinBot()
    result = bot.search(keyword='HUST')
    print(result)
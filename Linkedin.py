import undetected_chromedriver as uc
import chromedriver_autoinstaller
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config import *
import time
import random
from utils.utils import scroll_down

class LinkedinPost:
    def __init__(self, headless=False) -> None:
        chromedriver_autoinstaller.install()
        self.chrome_version = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
        self.driver = self._init_driver(headless)


    def _init_driver(self, headless):
        """Mở chương trình chrome

        Args:
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
        if headless:
            options.add_argument("--headless")
        driver = uc.Chrome(options=options,
                           version_main=self.chrome_version)
        return driver

    def get_list_url(self, keyword):
        list_url = []
        key_word = "+".join(keyword.split(" "))
        for x in range(0, 20, 10):

            self.driver.get(
                f'https://www.google.com/search?q=site:linkedin.com/posts/+inurl:/in/+intitle:{key_word}&rlz=1C1PNBB_enVN960VN960&sxsrf=APwXEdcEHsKS8i_rxEk_shM9UPJHZ2bvxw:1684831565326&ei=TX1sZIq9E92j2roPg-qkwA8&start={x}&sa=N&ved=2ahUKEwjKl9TXhov_AhXdkVYBHQM1CfgQ8tMDegQIDBAE&biw=958&bih=955&dpr=1')

            time.sleep(random.uniform(2.5, 4.9))
            # linkedin_urls = self.driver.find_elements('xpath', '//div[@class="yuRUbf"]/a')
            linkedin_urls = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="yuRUbf"]/a')))
            for link in linkedin_urls:
                list_url.append(link.get_attribute('href'))
            time.sleep(10)
        return list_url

    def login(self, credential):
        """Đăng nhập tài khoản linkedin
        Args:
            credential(dict): Thông tin tài khoản bao gồm email và password
        """
        self.driver.get("https://www.linkedin.com/login")
        # Email
        email_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
        email_field.send_keys(credential['email'])
        # Password
        password_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys(credential['password'])
        password_field.send_keys(Keys.RETURN)
        WebDriverWait(self.driver, 10).until(EC.title_contains("LinkedIn"))

    def _get_title(self):
        """Lấy tên người đăng bài post

        Returns:
            Str: Tên người post bài, nếu không lấy được thì trả về None
        """
        titles = self.driver.find_elements('xpath', '//span[contains(@class, "actor__title")]')
        if titles:
            title = titles[0].text.split('\n')[0]
            return title
        return None

    def _get_content(self):
        """Lấy nội dung trong bài post

        Returns:
            Str: Nội dung bài post, nếu không có trả về None
        """
        contents= self.driver.find_elements('xpath', '//span[@class="break-words"]')
        if contents:
            return contents[0].text
        return None

    def _get_reaction_count(self):
        """Số lượng phản ứng ứng (reaction)

        Returns:
            Str: Số lượng reaction nếu có, không thì trả về None
        """
        reactions = self.driver.find_elements('xpath', '//span[contains(@class, "reactions-count")]')
        if reactions:
            return reactions[0].text
        return None

    def _get_comment(self):
        """Lấy bình luận

        Returns:
            List[dict]: Danh sách các bình luận nếu có, không thì trả về None
        """
        scroll_down(self.driver)
        result = []
        comment_list = self.driver.find_elements('xpath',
                                                 '//div[contains(@class, "comments-comments-list")]//article[contains(@class, "comments-comment-item")]')
        for comment in comment_list:
            try:
                item = {}
                item['name'] = comment.find_element('xpath', '//span[contains(@class, "comments-post-meta__name-text")]').text
                item['comment'] = comment.find_element('xpath', '//span[contains(@class, "comments-comment-item__main-content")]').text
                result.append(item)
            except Exception as ex:
                continue
        return result if result else None

    def seach(self, url):
        """Thu thập nội dung bài post theo post url

        Args:
            url: url của bài post
        Returns:
            Dict: thông tin bài post
        """
        try:
            self.driver.get(url)
            # Wait for the search results page to load
            time.sleep(random.randint(2,3))
            post = {}
            post['title'] = self._get_title()
            post['content'] = self._get_content()
            post['reaction_count'] = self._get_reaction_count()
            post['comment'] = self._get_comment()
            return post
        except Exception as ex:
            print('Not exist result')
            return None

if __name__ == '__main__':
    bot = LinkedinPost()
    bot.login({'email': 'beomik0123@gmail.com', 'password':'tranmanhhieu238'})
    result = bot.seach(url='https://www.linkedin.com/posts/asif-bhat_going-pro-in-data-science-activity-6584710581549404160-H0za/')
    print(result)